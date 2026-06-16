# ResearchOS — Multi-Agent Research Intelligence Platform

ResearchOS is an AI-powered multi-agent research system that automates the process of information gathering, analysis, report generation, and evaluation.

Built using LangChain, Groq, Tavily Search, and Streamlit, the platform coordinates multiple AI agents to transform a simple research query into a structured and insightful research report.

---

## Features

✅ Multi-Agent Research Workflow

✅ Web Search Integration using Tavily

✅ Intelligent Content Extraction using BeautifulSoup

✅ AI-Powered Research Report Generation

✅ Automated Report Critique & Evaluation

✅ Professional Streamlit Dashboard

✅ Downloadable Research Reports

---

## Architecture

```text
User Query
    │
    ▼
Search Agent
    │
    ▼
Reader Agent
    │
    ▼
Writer Agent
    │
    ▼
Critic Agent
    │
    ▼
Final Research Report
```

### Agent Responsibilities

#### Search Agent

* Searches the web for recent and reliable information.
* Collects relevant sources and snippets.

#### Reader Agent

* Extracts detailed content from selected web sources.
* Cleans and prepares information for report generation.

#### Writer Agent

* Generates a structured research report.
* Produces clear and professional summaries.

#### Critic Agent

* Reviews the generated report.
* Provides feedback, strengths, improvement areas, and a quality score.

---

## Tech Stack

| Technology           | Purpose              |
| -------------------- | -------------------- |
| Python               | Core Development     |
| LangChain            | Agent Orchestration  |
| Groq (Llama 3.3 70B) | Large Language Model |
| Tavily Search API    | Web Search           |
| BeautifulSoup        | Web Scraping         |
| Streamlit            | User Interface       |


---

## Installation

### Clone Repository

```bash
git clone https://github.com/manasi-navale2107/ResearchOS.git

cd ResearchOS
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / macOS

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the root directory.

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

---

## Run Application

```bash
streamlit run app.py
```

---

## Example Workflow

1. Enter a research topic.
2. Search Agent gathers information from the web.
3. Reader Agent extracts detailed content.
4. Writer Agent generates a structured report.
5. Critic Agent evaluates the report.
6. Download the final report.

---

## Learning Outcomes

Through building ResearchOS, I gained hands-on experience with:

* Agentic AI Systems
* LangChain Agents
* Tool Calling
* Prompt Engineering
* Multi-Agent Workflows
* LLM Application Development
* Web Search Integration
* AI-Powered Research Automation

---

## Future Enhancements

* Multi-source content aggregation
* PDF export support
* Research history tracking
* Citation management
* Advanced analytics dashboard
* LangGraph-based workflow orchestration

---

## Author

**Manasi Navale**

Artificial Intelligence & Data Science Student
Passionate about Generative AI, Agentic Systems, Machine Learning, and AI Application Development.

---


