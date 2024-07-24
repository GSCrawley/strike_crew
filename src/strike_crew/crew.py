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

        agents = [
            Agent(
                config=agents_config['osint_analyst'],
                verbose=True,
                tools=[SerperDevTool()]
            ),
            Agent(
                config=agents_config['validation_agent'],
                verbose=True,
                tools=[neo4j_tool]
            ),
            # Agent(
            #     config=agents_config['knowledge_graph_agent'],
            #     verbose=True,
            #     tools=[knowledge_graph_tool]
            # )
        ]

        tasks = [
            Task(
                description="Gather intelligence on targets",
                expected_output="A list with bullet points containing the most relevant Twitter posts indicating the most recent Cybersecurity threats",
                tools=[SerperDevTool()],
                agent=agents[0]
            ),
            Task(
                description="Validate the intelligence gathered by the OSINT agent",
                expected_output="A confirmation that the gathered information matches known cyberattack techniques",
                tools=[neo4j_tool],
                agent=agents[1]
            )
        ]

        # Initialize the Crew base class with agents and tasks
        super().__init__(agents=agents, tasks=tasks, process=Process.hierarchical, verbose=2)
