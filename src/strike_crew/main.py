#!/usr/bin/env python
import sys
import os
from strike_crew.models import EmergingThreat
from strike_crew.crew import StrikeCrew, Agent
from strike_crew.tools.custom_tool import Neo4JSearchTool, WebSearchTool, WebScraperTool, DiffbotNLPTool, DiffbotGraphUpdateTool
from strike_crew.config_loader import load_config
import yaml

def main():
    agents_config_path = 'src/strike_crew/config/agents.yaml'
    tasks_config_path = 'src/strike_crew/config/tasks.yaml'

    agents_config = load_config(agents_config_path)
    tasks_config = load_config(tasks_config_path)

    api_key = os.getenv('SERPER_API_KEY')
    neo4j_uri = os.getenv('NEO4J_URI')
    neo4j_user = os.getenv('NEO4J_USER')
    neo4j_password = os.getenv('NEO4J_PASSWORD')
     
    # Initialize agents and tasks
    osint_analyst_tools = [
        WebSearchTool(api_key=api_key)
    ]
    validation_agent_tools = [
        Neo4JSearchTool(uri=neo4j_uri, user=neo4j_user, password=neo4j_password)
    ]
    osint_scraper_tools = [
        WebScraperTool()
    ]
    knowledge_graph_tools = [
        DiffbotNLPTool(), 
        DiffbotGraphUpdateTool(uri=neo4j_uri, user=neo4j_user, password=neo4j_password)
    ]

    osint_analyst_config = {k: v for k, v in agents_config['agents']['osint_analyst'].items() if k != 'tools'}
    osint_analyst = Agent(
        config=osint_analyst_config,
        verbose=True,
        tools=osint_analyst_tools
    )

    validation_agent_config = {k: v for k, v in agents_config['agents']['validation_agent'].items() if k != 'tools'}
    validation_agent = Agent(
        config=validation_agent_config,
        verbose=True,
        tools=validation_agent_tools
    )

    osint_scraper_config = {k: v for k, v in agents_config['agents']['osint_scraper_agent'].items() if k != 'tools'}
    osint_scraper = Agent(
        config=osint_scraper_config,
        verbose=True,
        tools=osint_scraper_tools
    )

    knowledge_graph_config = {k: v for k, v in agents_config['agents']['knowledge_graph_agent'].items() if k != 'tools'}
    knowledge_graph = Agent(
        config=knowledge_graph_config,
        verbose=True,
        tools=knowledge_graph_tools
    )


    # Initialize tasks
    tasks = [

    ]


    # Debug: Print the loaded configurations
    print("Agents Config:", agents_config)
    print("Tasks Config:", tasks_config)

    # # Initialize the StrikeCrew with loaded configurations
    strike_crew = StrikeCrew(agents_config, tasks_config)
    
    # Kickoff the crew process
    result = strike_crew.run()
    print(result)

if __name__ == "__main__":
    main()
