
import json
import requests
import streamlit as st

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2:3b"

st.set_page_config(
    page_title="AI Side-Hustle Assistant",
    page_icon="💡",
    layout="wide",
)

st.title("💡 AI Side-Hustle Assistant")
st.write(
    "Turn client requirements into a freelance proposal, "
    "task plan, estimated budget, and scope risk report."
)

project_name = st.text_input("Project name")

requirements = st.text_area(
    "Describe your client's requirements",
    placeholder="Example: Build a portfolio website quickly. "
    "We may add more features later.",
    height=150,
)

if st.button("Generate Project Plan", type="primary"):

    if not project_name.strip() or not requirements.strip():
        st.warning("Please enter both the project name and requirements.")

    else:
        prompt = f"""
You are a careful freelance project planner and scope analyst.

PROJECT NAME:
{project_name}

CLIENT REQUIREMENTS:
{requirements}

Return ONLY valid JSON using the exact schema below.
Do not use Markdown fences or text outside the JSON.

{{
  "overview": "Short project overview",
  "proposal": "Professional proposal for the client",
  "deliverables": ["Required deliverable"],
  "tasks": [
    {{
      "task": "Task name",
      "description": "What needs to be done",
      "days": 2,
      "cost_inr": 5000
    }}
  ],
  "questions": ["Question to clarify with the client"],
  "scope_risks": [
    {{
      "risk": "Unclear deadline",
      "severity": "High",
      "reason": "Why this creates uncertainty",
      "question": "Question to ask the client"
    }}
  ],
  "optional_recommendations": ["Optional improvement"]
}}

PLANNING RULES:
1. Treat the client's stated requirements as the source of truth.
2. Include only requested features and necessary implementation work
   as required deliverables.
3. Do not add login, a database, a backend, a CMS, payments, a blog,
   or other infrastructure unless the requirements need it.
4. For static portfolio and informational websites, prefer a
   frontend-only implementation unless more is requested.
5. Put unrequested enhancements under optional_recommendations.
6. Never present optional ideas as mandatory client requirements.

7. Check the brief separately for:
   - Vague or missing deadlines.
   - Unclear, incomplete, or changing requirements.
   - Missing or uncertain budget information.
   - Missing frequency or deliverables for recurring work.

8. When the brief explicitly contains one of these issues,
   create a separate scope_risks entry for it.

9. For an uncertain budget, explain that the budget has not
   been confirmed. Ask the client for a specific budget range.
   Do not claim the project is unprofitable without evidence.

10. Use severity High, Medium, or Low based on the likely
    impact. Explain each risk and provide a relevant question.
    Do not invent risks that are unsupported by the brief.

11. If there are no meaningful scope risks, return an empty
    scope_risks array.
12. Include positive whole numbers for days and non-negative
    whole numbers for cost_inr.
13. Include at least one practical task.
14. Keep tasks in implementation order.
15. Do not include calculated totals in the JSON.
    The application calculates totals from the task values.
16. Ask questions when technical choices are unclear rather than
    inventing client details.
17. All prices are estimates in Indian rupees (INR).
"""

        try:
            with st.spinner("Generating your project plan with Ollama..."):
                response = requests.post(
                    OLLAMA_URL,
                    json={
                        "model": MODEL,
                        "prompt": prompt,
                        "format": "json",
                        "stream": False,
                        "options": {"temperature": 0.2},
                    },
                    timeout=300,
                )
                response.raise_for_status()

                response_data = response.json()
                data = json.loads(response_data["response"])

            if not isinstance(data, dict):
                st.error("The AI returned an invalid project plan.")
                st.stop()

            tasks = data.get("tasks", [])
            scope_risks = data.get("scope_risks", [])
            deliverables = data.get("deliverables", [])
            questions = data.get("questions", [])
            recommendations = data.get("optional_recommendations", [])

            if not isinstance(tasks, list) or not tasks:
                st.error("The AI returned no tasks. Please try again.")
                st.stop()

            if not isinstance(scope_risks, list):
                scope_risks = []

            if not isinstance(deliverables, list):
                deliverables = []

            if not isinstance(questions, list):
                questions = []

            if not isinstance(recommendations, list):
                recommendations = []

            # Validate and normalize task estimates.
            validated_tasks = []

            for task in tasks:
                if not isinstance(task, dict):
                    continue

                try:
                    days = int(task.get("days", 1))
                    cost = int(task.get("cost_inr", 0))
                except (ValueError, TypeError, OverflowError):
                    continue

                if days < 1 or cost < 0:
                    continue

                validated_tasks.append({
                    "task": str(task.get("task", "Untitled task")),
                    "description": str(
                        task.get("description", "No description provided.")
                    ),
                    "days": days,
                    "cost_inr": cost,
                })

            if not validated_tasks:
                st.error(
                    "The AI returned no valid tasks. Please generate the plan again."
                )
                st.stop()

            # Normalize scope risk information.
            validated_risks = []

            for risk in scope_risks:
                if not isinstance(risk, dict):
                    continue

                severity = str(risk.get("severity", "Medium")).title()

                if severity not in ("High", "Medium", "Low"):
                    severity = "Medium"

                validated_risks.append({
                    "risk": str(risk.get("risk", "Scope uncertainty")),
                    "severity": severity,
                    "reason": str(
                        risk.get("reason", "Further clarification may be needed.")
                    ),
                    "question": str(
                        risk.get(
                            "question",
                            "Could you clarify this requirement?",
                        )
                    ),
                })

            total_days = sum(task["days"] for task in validated_tasks)
            total_budget = sum(
                task["cost_inr"] for task in validated_tasks
            )

            # Build the final downloadable plan from validated values.
            data["tasks"] = validated_tasks
            data["scope_risks"] = validated_risks
            data["deliverables"] = deliverables
            data["questions"] = questions
            data["optional_recommendations"] = recommendations
            data["estimated_workdays"] = total_days
            data["estimated_budget_inr"] = total_budget

            st.success("Your project plan is ready!")
            st.subheader("📋 Project Dashboard")

            overview_tab, proposal_tab, tasks_tab, budget_tab, risks_tab = (
                st.tabs([
                    "Overview",
                    "Proposal",
                    "Tasks & Timeline",
                    "Budget",
                    "⚠️ Scope Risks",
                ])
            )

            with overview_tab:
                st.markdown(
                    data.get("overview", "No overview provided.")
                )

                metric1, metric2 = st.columns(2)

                metric1.metric("Estimated workdays", total_days)
                metric2.metric(
                    "Estimated budget",
                    f"₹{total_budget:,}",
                )

                st.caption(
                    "These are estimates, not guaranteed delivery dates "
                    "or client quotes. Actual costs depend on scope, rates, "
                    "revisions, and client feedback."
                )

                st.markdown("### Required deliverables")

                if deliverables:
                    for item in deliverables:
                        st.markdown(f"- {item}")
                else:
                    st.info("No deliverables were returned.")

            with proposal_tab:
                st.markdown(
                    data.get("proposal", "No proposal provided.")
                )

                st.markdown("### Questions for the client")

                if questions:
                    for question in questions:
                        st.markdown(f"- {question}")
                else:
                    st.info("No clarification questions were returned.")

            with tasks_tab:
                st.dataframe(
                    [
                        {
                            "Task": task["task"],
                            "Description": task["description"],
                            "Estimated days": task["days"],
                            "Estimated cost (INR)": task["cost_inr"],
                        }
                        for task in validated_tasks
                    ],
                    use_container_width=True,
                    hide_index=True,
                )

                st.caption(
                    "Workdays are summed estimates, not calendar dates. "
                    "Tasks may overlap in a real project."
                )

            with budget_tab:
                st.dataframe(
                    [
                        {
                            "Task": task["task"],
                            "Estimated cost (INR)": task["cost_inr"],
                        }
                        for task in validated_tasks
                    ],
                    use_container_width=True,
                    hide_index=True,
                )

                st.metric(
                    "Total estimated budget",
                    f"₹{total_budget:,}",
                )

                st.markdown("### Optional recommendations")

                if recommendations:
                    for item in recommendations:
                        st.markdown(f"- {item}")
                else:
                    st.info("No optional recommendations provided.")

            with risks_tab:
                st.subheader("Scope Risk Checker")

                st.write(
                    "Review uncertainties before agreeing to the project."
                )

                if not validated_risks:
                    st.success("No major scope risks detected by the AI.")

                else:
                    for index, risk in enumerate(validated_risks, start=1):
                        with st.container(border=True):
                            st.markdown(
                                f"**{index}. {risk['risk']}**"
                            )

                            severity = risk["severity"]

                            if severity == "High":
                                st.error("Severity: High")
                            elif severity == "Medium":
                                st.warning("Severity: Medium")
                            else:
                                st.info("Severity: Low")

                            st.write(risk["reason"])

                            st.markdown(
                                "**Question to ask the client:**"
                            )
                            st.write(risk["question"])

                st.caption(
                    "AI-generated risk analysis may miss issues. "
                    "Review the client's actual requirements before quoting."
                )

            st.download_button(
                "Download project plan (JSON)",
                data=json.dumps(
                    data,
                    indent=2,
                    ensure_ascii=False,
                ),
                file_name="project_plan.json",
                mime="application/json",
            )

        except requests.exceptions.ConnectionError:
            st.error(
                "Cannot connect to Ollama. Make sure Ollama is running "
                "and the model is installed."
            )

        except requests.exceptions.Timeout:
            st.error(
                "The AI took too long to respond. Please try again."
            )

        except requests.exceptions.RequestException as error:
            st.error(f"Ollama request failed: {error}")

        except (ValueError, KeyError, TypeError) as error:
            st.error(
                "The AI returned data in an unexpected format. "
                "Please try again."
            )
