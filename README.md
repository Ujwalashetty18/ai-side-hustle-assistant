# 💡 AI Side-Hustle Assistant

An AI-powered freelance planning tool that transforms client requirements into a project proposal, task breakdown, estimated budget, and scope risk analysis.

Built with **Python, Streamlit, and Ollama**, using the open-weight Llama 3.2 model locally.

## ✨ Features

- **AI Project Proposal:** Generate a professional proposal from a client's brief.
- **Task Planning:** Break projects into practical tasks and estimated workdays.
- **Budget Estimation:** Calculate an estimated budget in Indian rupees from task-level costs.
- **Scope Risk Checker:** Identify uncertainties such as vague deadlines, changing requirements, and missing budget details.
- **Client Clarification Questions:** Suggest questions to ask before accepting a project.
- **Optional Recommendations:** Separate extra ideas from required deliverables.
- **Project Plan Export:** Download the generated plan as a JSON file.

## 🛠️ Tech Stack

- Python
- Streamlit
- Ollama
- Llama 3.2 (3B)
- Requests

## ⚙️ Prerequisites

Install Python and Git. Install [Ollama](https://ollama.com/) and download the model:

```bash
ollama pull llama3.2:3b
```

## 🚀 Run Locally

Clone the repository:

```bash
git clone https://github.com/Ujwalashetty18/ai-side-hustle-assistant.git
cd ai-side-hustle-assistant
```

Create and activate a virtual environment.

**Windows — Git Bash:**

```bash
py -m venv venv
source venv/Scripts/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Make sure Ollama is running, then start the application:

```bash
streamlit run app.py
```

Open the local URL shown in the terminal, usually `http://localhost:8501`.

## 🧪 Example Use Case

A bakery owner wants a website with a product menu, prices, opening hours, location, and a contact form.

The assistant generates a proposal, implementation tasks, estimated costs, questions for the client, and possible scope risks.

## ⚠️ Limitations

- Budgets and timelines are estimates, not guaranteed quotes.
- AI-generated plans and risk assessments may contain mistakes or miss issues.
- Review the plan and confirm requirements with the client before making commitments.
- The local setup requires Ollama and the downloaded model.

## 🌱 Why Open Innovation Matters

Running an open-weight model locally gives developers more control over their tools and data. The project can be inspected, modified, and extended by other developers.

## 📄 License

See the `LICENSE` file for the project's open-source license.

## 👩‍💻 Author

**Ujwala Shetty**

GitHub: [Ujwalashetty18](https://github.com/Ujwalashetty18)

---

Built as part of the Hacktoberfest 2026 Side Hustle challenge.
