
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
st.write("Create a freelance proposal, task plan, timeline, and budget.")

project_name = st.text_input("Project name")
requirements = st.text_area(
    "Describe your client's requirements",
    placeholder="Example: Build a website for a local bakery...",
    height=150,
)

if st.button("Generate Project Plan", type="primary"):
    if not project_name.strip() or not requirements.strip():
        st.warning("Please enter both the project name and requirements.")
    else:
        prompt = f"""
You are a careful freelance project planner.

Create a plan for this project.
Project name: {project_name}
Client requirements: {requirements}

Return ONLY valid JSON, without markdown fences, using this schema:
{{
  "overview": "short project overview",
  "proposal": "professional client proposal",
  "deliverables": ["deliverable 1"],
  "tasks": [
    {{
      "task": "task name",
      "description": "what must be done",
      "days": 2,
      "cost_inr": 5000
    }}
  ],
  "questions": ["question for the client"],
  "optional_recommendations": ["optional idea"]
}}


Rules:
- Treat the client's requirements as the source of truth.
- Include only explicitly requested features as required deliverables.
- Do not add a backend, database, CMS, login, payment system, or other infrastructure unless the requirements need it.
- For a static portfolio or informational website, prefer a frontend-only solution unless the client requests more.
- Put unrequested features and enhancements only in optional_recommendations.
- Do not turn implementation suggestions into required deliverables.
- Use positive whole numbers for days and cost_inr.
- Keep tasks practical and in implementation order.
- Do not include a total budget or total timeline in the JSON; the application calculates these.
- Do not invent client details.
- If a technical decision is unclear, mention it in questions rather than assuming it is required.
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
                data = json.loads(response.json()["response"])

            tasks = data.get("tasks", [])
            if not isinstance(tasks, list) or not tasks:
                st.error("The AI returned no tasks. Please try again.")
                st.stop()

            for task in tasks:
                task["days"] = max(1, int(task["days"]))
                task["cost_inr"] = max(0, int(task["cost_inr"]))

            total_days = sum(task["days"] for task in tasks)
            total_budget = sum(task["cost_inr"] for task in tasks)

            st.success("Your project plan is ready!")
            st.subheader("📋 Project Dashboard")

            overview_tab, proposal_tab, tasks_tab, budget_tab = st.tabs(
                ["Overview", "Proposal", "Tasks & Timeline", "Budget"]
            )

            with overview_tab:
                st.markdown(data.get("overview", "No overview provided."))
                st.metric("Estimated workdays", total_days)
                st.metric("Estimated budget", f"₹{total_budget:,}")
                st.caption(
                    "Estimates only. Actual costs and dates depend on "
                    "scope, rates, revisions, and client feedback."
                )

                st.markdown("### Required deliverables")
                for item in data.get("deliverables", []):
                    st.markdown(f"- {item}")

            with proposal_tab:
                st.markdown(data.get("proposal", "No proposal provided."))

                st.markdown("### Questions for the client")
                for question in data.get("questions", []):
                    st.markdown(f"- {question}")

            with tasks_tab:
                st.dataframe(
                    [
                        {
                            "Task": task["task"],
                            "Description": task["description"],
                            "Estimated days": task["days"],
                            "Estimated cost (INR)": task["cost_inr"],
                        }
                        for task in tasks
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
                        for task in tasks
                    ],
                    use_container_width=True,
                    hide_index=True,
                )
                st.metric("Total estimated budget", f"₹{total_budget:,}")

                st.markdown("### Optional recommendations")
                for item in data.get("optional_recommendations", []):
                    st.markdown(f"- {item}")

                st.download_button(
                    "Download project plan (JSON)",
                    data=json.dumps(data, indent=2, ensure_ascii=False),
                    file_name="project_plan.json",
                    mime="application/json",
                )

        except requests.exceptions.ConnectionError:
            st.error("Cannot connect to Ollama. Check that Ollama is running.")
        except requests.exceptions.Timeout:
            st.error("The AI took too long to respond. Please try again.")
        except requests.exceptions.RequestException as error:
            st.error(f"Ollama request failed: {error}")
        except (ValueError, KeyError, TypeError) as error:
            st.error(
                "The AI returned data in an unexpected format. "
                "Please click Generate Project Plan again."
            )
