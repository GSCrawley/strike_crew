from crewai import Agent, Crew, Process, Task
from typing import Dict, Any
from strike_crew.tools.custom_tool import (
    Neo4JSearchTool, WebSearchTool, WebScraperTool, 
    DiffbotNLPTool, DiffbotGraphUpdateTool
)
from pydantic import BaseModel, Field

from dotenv import load_dotenv
import os
from groq import Groq

# Load environment variables from .env file
load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
api_key = os.environ.get("GOOGLE_SERPER_API_KEY")

 # Neo4j credentials
neo4j_uri = os.environ.get("NEO4J_URI")
neo4j_user = os.environ.get("NEO4J_USER")
neo4j_password = os.environ.get("NEO4J_PASSWORD")

class StrikeCrew(Crew):
    crew_manager_config: Dict[str, Any] = Field(...)
    tasks_config: Dict[str, Any] = Field(...)
    def __init__(self, agents_config: Dict[str, Any], tasks_config: Dict[str, Any]):
        # super().__init__(crew_manager_config=agents_config['agents']['crew_manager'], tasks_config=tasks_config)

        # print("Initializing Crew with agents_config:", agents_config)
        if 'crew_manager' not in agents_config.get('agents', {}):
            raise KeyError("'crew_manager' key not found in agents_config['agents']")
        
        self.crew_manager_config = agents_config['agents']['crew_manager']
        self.tasks_config = tasks_config

        osint_analyst_tools = {
            "Web Search": WebSearchTool(api_key)
        }

        validation_agent_tools = {
            "Neo4J Search": Neo4JSearchTool(neo4j_uri, neo4j_user, neo4j_password)
        }

        osint_scraper_tools = {
            "Web Scraper": WebScraperTool()
        }

        knowledge_graph_tools = {
            "NLP Tool": DiffbotNLPTool(),
            "Neo4J Update": DiffbotGraphUpdateTool(neo4j_uri, neo4j_user, neo4j_password)
        }

        osint_analyst = Agent(
            config=agents_config['agents']['osint_analyst'],
            verbose=True,
            tools=osint_analyst_tools
        )

        validation_agent = Agent(
            config=agents_config['agents']['validation_agent'],
            verbose=True,
            tools=validation_agent_tools
        )

        osint_scraper_agent = Agent(
            config=agents_config['agents']['osint_scraper_agent'],
            verbose=True,
            tools=osint_scraper_tools
        )

        knowledge_graph_agent = Agent(
            config=agents_config['agents']['knowledge_graph_agent'],
            verbose=True,
            tools=knowledge_graph_tools
        )

        agents = [osint_analyst, validation_agent, osint_scraper_agent, knowledge_graph_agent]

        search_task = Task(
            description=tasks_config['tasks']['search_task']['description'],
            expected_output=tasks_config['tasks']['search_task']['expected_output']
        )

        validation_task = Task(
            description=tasks_config['tasks']['validation_task']['description'],
            expected_output=tasks_config['tasks']['validation_task']['expected_output']
        )

        scraping_task = Task(
            description=tasks_config['tasks']['scraping_task']['description'],
            expected_output=tasks_config['tasks']['scraping_task']['expected_output']
        )

        nlp_task = Task(
            description=tasks_config['tasks']['nlp_task']['description'],
            expected_output=tasks_config['tasks']['nlp_task']['expected_output']
        )

        graph_update_task = Task(
            description=tasks_config['tasks']['graph_update_task']['description'],
            expected_output=tasks_config['tasks']['graph_update_task']['expected_output']
        )

        tasks = [search_task, validation_task, scraping_task, nlp_task, graph_update_task]

        # Initialize the Crew base class with agents and tasks
        super().__init__(agents=agents, tasks=tasks, process=Process.hierarchical, verbose=2)

# Example usage
if __name__ == "__main__":
    agents_config = {
        'agents': {
            'crew_manager': {
                'name': 'crew_manager',
                'role': 'Crew Manager\n',
                'goal': 'Manage and coordinate all other agents.\n',
                'backstory': 'Skilled in orchestrating complex processes and ensuring smooth collaboration between agents.\n'
            },
            'osint_analyst': {
                'name': 'osint_analyst',
                'role': 'OSINT Analyst\n',
                'goal': 'Search for sources of information containing intelligence on cybersecurity threats.\n',
                'backstory': 'You are a sophisticated AI-powered agent responsible for scouring the internet to gather vital information on emerging threats; experienced in identifying and gathering intelligence from open-source data about current, recent, historical and emerging cybersecurity threats, uncovering the latest discussions and trends surrounding Threat Actors, Campaigns, Indicators of Compromise (IoCs), and Tactics, Techniques, and Procedures (TTPs). With its advanced algorithms and natural language processing capabilities, the OSINT Analyst Agent can swiftly sift through the noise to identify relevant information.\n',
                'tools': ['custom_tool.WebSearchTool']
            },
            'osint_scraper_agent': {
                'name': 'osint_scraper_agent',
                'role': 'OSINT Information Gathering\n',
                'goal': 'Gather and scrape information from various sources.\n',
                'backstory': 'Expert in extracting data from multiple sources to provide comprehensive intelligence.\n',
                'tools': ['custom_tool.WebScraperTool']
            },
            'validation_agent': {
                'name': 'validation_agent',
                'role': 'Validation Agent\n',
                'goal': 'Verify the accuracy and relevance of the intelligence gathered by the OSINT agents.\n',
                'backstory': 'Expert in verifying the accuracy and relevance of the intelligence gathered by the OSINT agents.\n',
                'tools': ['custom_tool.Neo4JSearchTool']
            },
            'knowledge_graph_agent': {
                'name': 'knowledge_graph_agent',
                'role': 'Knowledge Graph Agent\n',
                'goal': 'Create a knowledge graph from the intelligence gathered by the OSINT agents.\n',
                'backstory': 'Expert in creating a knowledge graph from the intelligence gathered by the OSINT agents.\n',
                'tools': ['custom_tool.DiffbotGraphUpdateTool', 'custom_tool.DiffbotNLPTool']
            }
        }
    }

    tasks_config = {
        'tasks': {
            'search_task': {
                'name': 'SearchTask',
                'description': 'Search the web for information on cybersecurity threats based on user queries and provide a list of URLs.\n',
                'expected_output': 'A list of URLs containing relevant information about cybersecurity threats.\n',
                'inputs': [{'name': 'query'}],
                'agent': 'osint_analyst'
            },
            'scraping_task': {
                'name': 'ScrapingTask',
                'description': 'Gather and scrape intelligence on cybersecurity threats from the provided URLs.\n',
                'expected_output': 'Extracted information from the URLs, including Threat Actors, Campaigns, IoCs, and TTPs.\n',
                'inputs': [{'name': 'urls'}],
                'agent': 'osint_scraper_agent'
            },
            'validation_task': {
                'name': 'ValidationTask',
                'description': 'Verify the accuracy and relevance of the intelligence gathered by the OSINT agents.\n',
                'expected_output': 'A list of verified intelligence data, cross-referenced with the Neo4J database.\n',
                'inputs': [{'name': 'intelligence'}],
                'agent': 'validation_agent'
            },
            'nlp_task': {
                'name': 'NLPTask',
                'description': 'Use Natural Language Processing to extract relevant information from the verified intelligence data.\n',
                'expected_output': 'Extracted information from the verified intelligence data, including Threat Actors, Campaigns, IoCs, and TTPs.\n',
                'inputs': [{'name': 'verified_intelligence'}],
                'agent': 'knowledge_graph_agent'
            },
            'graph_update_task': {
                'name': 'GraphUpdateTask',
                'description': 'Update the Neo4J database with new knowledge graphs based on the verified intelligence data.\n',
                'expected_output': 'Updated knowledge graphs in the Neo4J database representing relationships between Threat Actors, Campaigns, IoCs, TTPs, and CVEs.\n',
                'inputs': [{'name': 'verified_intelligence'}],
                'agent': 'knowledge_graph_agent'
            }
        }
    }

    crew = StrikeCrew(agents_config, tasks_config)
    crew.run()