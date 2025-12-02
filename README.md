# AIStrike_Crew - A Multi-Agent System for Cybersecurity and Threat Intelligence Gathering

### groq llama  https://github.com/groq-ai/groq-llama

### create more powerful custom scraping tool - blogs seem to be protected - scraper tool needs to be able to scrape from blogs

# https://blog.qualys.com/vulnerabilities-threat-research/2024/07/01/regresshion-remote-unauthenticated-code-execution-vulnerability-in-openssh-server

# Graph agent should generate a Neo4j cypher query to enter data into neo4j

# StrikeCrew Crew

Welcome to the StrikeCrew project. The current sprint focuses on a front-end “Threat Intelligence Radar” that keeps the data relevant and fresh by aggregating trusted cybersecurity feeds and ranking them by recency and severity. The legacy CrewAI research flow remains in the codebase, but the primary entry point now serves an interactive dashboard powered by a lightweight built-in web server.

## Installation

Ensure you have Python >=3.10 <=3.13 installed on your system. This project uses [Poetry](https://python-poetry.org/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install Poetry:

```bash
pip install poetry
```

Next, navigate to your project directory and install the dependencies:

1. First lock the dependencies and then install them:
```bash
poetry lock
```
```bash
poetry install
```
### Customizing

**Add your `OPENAI_API_KEY` into the `.env` file**

- Modify `src/strike_crew/config/agents.yaml` to define your agents
- Modify `src/strike_crew/config/tasks.yaml` to define your tasks
- Modify `src/strike_crew/crew.py` to add your own logic, tools and specific args
- Modify `src/strike_crew/main.py` to add custom inputs for your agents and tasks

## Running the Project

To launch the live dashboard from the project root:

```bash
poetry install
poetry run strike_crew
```

Then open http://localhost:8000 in your browser. The API endpoints are:

- `GET /api/feed` – returns the ranked feed of recent threat intelligence items.
- `GET /api/sources` – lists the curated sources powering the dashboard.

### Optional CSec_SaaS integration

If you have a running instance of [CSec_SaaS](https://github.com/GSCrawley/CSec_SaaS/tree/main/CSec_SaaS), you can pipe its feed
into the Threat Intelligence Radar by setting:

```bash
export CSEC_SAAS_BASE_URL="https://your-csec-saas-host"
# optional
export CSEC_SAAS_API_KEY="<token>"
```

With these environment variables present, the dashboard merges CSec_SaaS alerts with the curated RSS sources and surfaces them
in `/api/feed` and the UI automatically.

## Understanding Your Crew

The strike_crew Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.

## Support

For support, questions, or feedback regarding the StrikeCrew Crew or crewAI.
- Visit our [documentation](https://docs.crewai.com)
- Reach out to us through our [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join our Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with our docs](https://chatg.pt/DWjSBZn)

Let's create wonders together with the power and simplicity of crewAI.

