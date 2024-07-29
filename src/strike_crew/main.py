#!/usr/bin/env python
import sys
import os
from strike_crew.models import EmergingThreat
from strike_crew.crew import StrikeCrew, Agent
from strike_crew.tools.custom_tool import Neo4JSearchTool, WebSearchTool, WebScraperTool, DiffbotNLPTool, DiffbotGraphUpdateTool
from strike_crew.config_loader import load_config
import yaml
from strike_crew.workflow import ThreatIntelWorkflow
from crewai import Task, StrikeCrew, Process

def main():
    agents_config_path = 'src/strike_crew/config/agents.yaml'
    tasks_config_path = 'src/strike_crew/config/tasks.yaml'
    agents_config = load_config(agents_config_path)
    tasks_config = load_config(tasks_config_path)

    api_key = os.getenv('SERPER_API_KEY')
    neo4j_uri = os.getenv('NEO4J_URI')
    neo4j_user = os.getenv('NEO4J_USER')
    neo4j_password = os.getenv('NEO4J_PASSWORD')

    # Initialize tools
    web_search_tool = WebSearchTool(api_key=api_key)
    web_scraper_tool = WebScraperTool()
    neo4j_search_tool = Neo4JSearchTool(uri=neo4j_uri, user=neo4j_user, password=neo4j_password)
    diffbot_nlp_tool = DiffbotNLPTool()
    diffbot_graph_update_tool = DiffbotGraphUpdateTool(uri=neo4j_uri, user=neo4j_user, password=neo4j_password)


      # Initialize crew_manager
    crew_manager = Agent(
        name="Crew Manager",
        role="Manage and coordinate all other agents",
        goal="Orchestrate the threat intelligence gathering process",
        backstory="Expert in managing AI agent teams and coordinating complex cybersecurity workflows",
        verbose=True,
        allow_delegation=True
    )

    # Initialize other agents
    osint_analyst = Agent(
        name="OSINT Analyst",
        role="Search for cybersecurity threat information",
        goal="Find relevant and recent cybersecurity threat data",
        backstory="Expert in open-source intelligence gathering",
        verbose=True,
        allow_delegation=False,
        tools=[web_search_tool]
    )

    osint_scraper = Agent(
        name="OSINT Scraper",
        role="Scrape and extract information from web pages",
        goal="Gather detailed threat data from identified sources",
        backstory="Specialized in web scraping and data extraction",
        verbose=True,
        allow_delegation=False,
        tools=[web_scraper_tool]
    )

    validation_agent = Agent(
        name="Validation Agent",
        role="Verify and validate gathered threat intelligence",
        goal="Ensure accuracy and relevance of collected data",
        backstory="Expert in threat intelligence validation techniques",
        verbose=True,
        allow_delegation=False,
        tools=[neo4j_search_tool]
    )

    nlp_agent = Agent(
        name="NLP Agent",
        role="Process and analyze threat intelligence data",
        goal="Extract structured information from unstructured text",
        backstory="Specialized in natural language processing for cybersecurity",
        verbose=True,
        allow_delegation=False,
        tools=[diffbot_nlp_tool]
    )

    knowledge_graph_agent = Agent(
        name="Knowledge Graph Agent",
        role="Create and update threat intelligence knowledge graphs",
        goal="Maintain an up-to-date graph database of threat intelligence",
        backstory="Expert in graph databases and threat intelligence structuring",
        verbose=True,
        allow_delegation=False,
        tools=[diffbot_graph_update_tool]
    )

      # Initialize tasks
    search_task = Task(
        description="Search for latest cybersecurity threats",
        agent=osint_analyst
    )

    scrape_task = Task(
        description="Scrape detailed information from identified sources",
        agent=osint_scraper
    )

    validate_task = Task(
        description="Validate and verify the gathered threat intelligence",
        agent=validation_agent
    )

    nlp_task = Task(
        description="Process and analyze the threat intelligence data",
        agent=nlp_agent
    )

    graph_task = Task(
        description="Update the knowledge graph with new threat intelligence",
        agent=knowledge_graph_agent
    )

    # Create the crew with the crew_manager
    crew = StrikeCrew(
        agents=[osint_analyst, osint_scraper, validation_agent, nlp_agent, knowledge_graph_agent],
        tasks=[search_task, scrape_task, validate_task, nlp_task, graph_task],
        manager=crew_manager,
        process=Process.hierarchical,
        verbose=2
    )

    # Initialize the workflow with the crew
    workflow = ThreatIntelWorkflow(crew)

    # Run the workflow
    results = workflow.run("Latest cybersecurity threats")

    # Print results
    for threat in results:
        print(f"Emerging Threat: {threat}")

    # Optionally, run continuous monitoring
    # workflow.run_continuous(interval=3600)  # Run every hour

if __name__ == "__main__":
    main()