from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.tools import WebSearchTool
from strike_crew.tools.custom_tool import TwitterSearchTool, Neo4JSearchTool
import os

from groq import Groq

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool

@CrewBase
class StrikeCrew():
	"""StrikeCrew crew"""
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'
   
agents = []
tasks = []


# @agent
# def researcher(self) -> Agent:
#     return Agent(
#         config=self.agents_config['researcher'],
#         tools= WebSearchTool(), # Example of custom tool, loaded on the beginning of file
#         verbose=True
#     )

# @agent
# def reporting_analyst(self) -> Agent:
#     return Agent(
#         config=self.agents_config['reporting_analyst'],
#         verbose=True
    
#     )
 
@agent
def osint_analyst(self) -> Agent:   
    return Agent(
        config=self.agents_config['osint_analyst'],
        verbose=True,
        tools=[WebSearchTool(), TwitterSearchTool()]
    )

@task
def osint_task(self) -> Task:
    return Task(
        description="Gather intelligence on targets",
        expected_output="A list with bullet points containing the most relevant Twitter posts indicating the most recent Cybersecurity threats",
        tools=[WebSearchTool(), TwitterSearchTool()]
    )

@agent
def validation_agent(self) -> Agent:
    return Agent(
        config=self.agents_config['validation_agent'],
        verbose=True,
        tools=[Neo4JSearchTool()]
    )

@task
def validation_task(self) -> Task:
    return Task(
        description="Validate the intelligence gathered by the OSINT agent",
        expected_output="A confirmation that the gathered information matches known cyberattack techniques",
        tools=[Neo4JSearchTool()]
    )


@crew
def crew(self) -> Crew: 
    return Crew(
	agents=self.agents, # Automatically created by the @agent decorator
	tasks=self.tasks, # Automatically created by the @task decorator
	process=Process.sequential,
	verbose=2
    )
	# process=Process.se, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
