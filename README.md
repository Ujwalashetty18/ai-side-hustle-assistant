# 💡 AI Side-Hustle Assistant

An AI-powered freelance project planner built with Python, Streamlit, and Ollama.

## Features

- Generate professional freelance proposals.
- Create project deliverables and implementation tasks.
- Estimate project timelines and budgets in Indian rupees (INR).
- Identify questions to clarify with clients.
- Separate required deliverables from optional recommendations.
- Download the generated project plan as a JSON file.

## Technology Stack

- Python
- Streamlit
- Ollama
- Llama 3.2 (3B)
- Requests

## Prerequisites

- Python installed
- [Ollama](https://ollama.com/) installed
- Git installed

## Installation

Clone this repository and enter the project directory:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd ai-side-hustle-assistant
```

Create and activate a virtual environment.

On Windows:

```bash
py -m venv venv
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Download the AI model:

```bash
ollama pull llama3.2:3b
```

Start Ollama, then run the application:

```bash
streamlit run app.py
```

Open the local URL shown in your terminal.

## How It Works

Enter a project name and the client's requirements. The local AI model generates a proposal, deliverables, tasks, estimated workdays, and a budget. You can review the results in the dashboard and download the plan as JSON.

## Important Notes

- Project timelines and budgets are estimates, not guaranteed quotes.
- Review AI-generated plans before sharing them with clients.
- The application requires Ollama and the selected model to be available locally.

## License

License information will be added before publication.
