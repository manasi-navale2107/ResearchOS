# ResearchOS – Multi-Agent Research Intelligence Platform

ResearchOS is an AI-powered multi-agent research system that automates the process of gathering, analyzing, and synthesizing information from the web.

The platform coordinates multiple specialized AI agents to search for information, extract relevant content, generate structured reports, and critically evaluate the final output.

## Features

* Multi-Agent Research Workflow
* Web Search using Tavily
* Intelligent Content Extraction
* AI-Powered Report Generation
* Automated Report Critique & Evaluation
* Interactive Streamlit Dashboard

## Architecture

User Query
↓
Search Agent
↓
Reader Agent
↓
Writer Agent
↓
Critic Agent
↓
Final Research Report

## Tech Stack

* Python
* LangChain
* Groq (Llama 3.3 70B)
* Tavily Search API
* BeautifulSoup
* Streamlit

## Installation

```bash
git clone https://github.com/manasi-navale2107/ResearchOS.git

cd ResearchOS

pip install -r requirements.txt
```

Create a `.env` file:

```env
GROQ_API_KEY=your_key
TAVILY_API_KEY=your_key
```

Run:

```bash
streamlit run app.py
```

## Future Improvements

* Multi-source research aggregation
* PDF report export
* LangGraph-based workflow orchestration
* Citation management
* Research history tracking
