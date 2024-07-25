from crewai import Agent, Crew, Process, Task
from crewai_tools import SerperDevTool
from strike_crew.tools.custom_tool import Neo4JSearchTool
from dotenv import load_dotenv
import os
from groq import Groq

# Load environment variables from .env file
load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

 # Neo4j credentials
neo4j_uri = os.environ.get("NEO4J_URI")
neo4j_user = os.environ.get("NEO4J_USER")
neo4j_password = os.environ.get("NEO4J_PASSWORD")
# neo4j_encrypted = os.environ.get("NEO4J_ENCRYPTED") == "True"

class Crew:
    """StrikeCrew crew"""
    def __init__(self, agents_config, tasks_config):  
        # Debug: Print the agents_config to verify its structure
        print("Initializing Crew with agents_config:", agents_config)
        
        # Check if 'crew_manager' key exists
        if 'crew_manager' not in agents_config.get('agents', {}):
            raise KeyError("'crew_manager' key not found in agents_config['agents']")
        
        self.crew_manager_config = agents_config['agents']['crew_manager']
        self.tasks_config = tasks_config

         # Remove 'tools' from config before passing it to Agent
        osint_analyst_config = agents_config['agents']['osint_analyst'].copy()
        osint_analyst_tools = {tool.name: tool for tool in osint_analyst_tools}
        validation_agent_tools = {tool.name: tool for tool in validation_agent_tools}

        osint_analyst = Agent(
            config=osint_analyst_config,
            verbose=True,
            tools={SerperDevTool().name: SerperDevTool()} | osint_analyst_tools
        )

        validation_agent_config = agents_config['agents']['validation_agent'].copy()
        validation_agent_tools = validation_agent_config.pop('tools', [])

        validation_agent = Agent(
            config=validation_agent_config,
            verbose=True,
                tools={Neo4JSearchTool().name: Neo4JSearchTool()} | validation_agent_tools
        )

        agents = [osint_analyst, validation_agent]

        search_task = Task(
            description=tasks_config['tasks']['search_task']['description'],
            expected_output=tasks_config['tasks']['search_task']['expected_output']
        )

        validation_task = Task(
            description=tasks_config['tasks']['validation_task']['description'],
            expected_output=tasks_config['tasks']['validation_task']['expected_output']
        )

        tasks = [search_task, validation_task]

        # Initialize the Crew base class with agents and tasks
        super().__init__(agents=agents, tasks=tasks, process=Process.hierarchical, verbose=2)
