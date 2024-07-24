from crewai import Agent, Crew, Process, Task
from crewai_tools import SerperDevTool
from strike_crew.tools.custom_tool import Neo4JSearchTool
from dotenv import load_dotenv
import os
from groq import Groq

# Load environment variables from .env file
load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

class StrikeCrew(Crew):
    """StrikeCrew crew"""

    def __init__(self, agents_config, tasks_config):

        # Neo4j credentials
        neo4j_uri = os.environ.get("NEO4J_URI")
        neo4j_user = os.environ.get("NEO4J_USER")
        neo4j_password = os.environ.get("NEO4J_PASSWORD")
        # neo4j_encrypted = os.environ.get("NEO4J_ENCRYPTED") == "True"

        neo4j_tool = Neo4JSearchTool(
            uri = neo4j_uri,
            user = neo4j_user,
            password = neo4j_password,
            # encrypted = neo4j_encrypted
        )

        crew_manager_agent = Agent(
            config=agents_config['crew_manager_agent'],
            verbose=True,
            tools=[]
        )

        osint_analyst = Agent(
            config=agents_config['osint_analyst'],
            verbose=True,
            tools=[SerperDevTool()]
        )

        validation_agent = Agent(
            config=agents_config['validation_agent'],
            verbose=True,
            tools=[neo4j_tool]
        )

        agents = [crew_manager_agent, osint_analyst, validation_agent]

        search_task = Task(
            description=tasks_config['search_task']['description'],
            expected_output=tasks_config['search_task']['expected_output'],
            tools=[SerperDevTool()],
            agent=osint_analyst
        )

        validation_task = Task(
            description=tasks_config['validation_task']['description'],
            expected_output=tasks_config['validation_task']['expected_output'],
            tools=[neo4j_tool],
            agent=validation_agent
        )

        tasks = [search_task, validation_task]

        # Initialize the Crew base class with agents and tasks
        super().__init__(agents=agents, tasks=tasks, process=Process.hierarchical, verbose=2)
