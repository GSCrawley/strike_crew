from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

import os

from groq import Groq

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)


# Uncomment the following line to use an example of a custom tool
# from strike_crew.tools.custom_tool import NEO4JTool

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool

@CrewBase
class StrikeCrew():
	"""StrikeCrew crew"""
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['researcher'],
			# tools=[MyCustomTool()], # Example of custom tool, loaded on the beginning of file
			verbose=True
		)

	@agent
	def reporting_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['reporting_analyst'],
			verbose=True
		)
    
    @agent
    def osint_analyst_1(self) -> Agent:
        return Agent(
            config=self.agents_config['osint_analyst_1'],
            verbose=True
        )

    @agent
    def osint_analyst_2(self) -> Agent:
        return Agent(
            config=self.agents_config['osint_analyst_2'],
            verbose=True
        )

    @agent
    def osint_analyst_3(self) -> Agent:
        return Agent(
            config=self.agents_config['osint_analyst_3'],
            verbose=True
        )

    @agent
    def reputation_analysis_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['reputation_analysis_agent'],
            verbose=True
        )

    @agent
    def contextual_enrichment_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['contextual_enrichment_agent'],
            verbose=True
        )

    @agent
    def threat_validation_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['threat_validation_agent'],
            verbose=True
        )

    @agent
    def threat_analysis_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['threat_analysis_agent'],
            verbose=True
        )

    @agent
    def knowledge_graph_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['knowledge_graph_agent'],
            verbose=True
        )


    @task
    def research_task(self) -> Task:
    	return Task(
			config=self.tasks_config['research_task'],
			agent=self.researcher()
		)
    
    @task
    def reporting_task(self) -> Task:
	    return Task(
			config=self.tasks_config['reporting_task'],
			agent=self.reporting_analyst(),
			output_file='report.md'
		)

    @task
    def osint_task_1(self) -> Task:
        return Task(
            config=self.tasks_config['osint_task_1'],
            agent=self.osint_analyst_1()
        )

    @task
    def osint_task_2(self) -> Task:
        return Task(
            config=self.tasks_config['osint_task_2'],
            agent=self.osint_analyst_2()
        )

    @task
    def osint_task_3(self) -> Task:
        return Task(
            config=self.tasks_config['osint_task_3'],
            agent=self.osint_analyst_3()
        )

    @task
    def reputation_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['reputation_analysis_task'],
            agent=self.reputation_analysis_agent()
        )

    @task
    def contextual_enrichment_task(self) -> Task:
        return Task(
            config=self.tasks_config['contextual_enrichment_task'],
            agent=self.contextual_enrichment_agent()
        )

    @task
    def threat_validation_task(self) -> Task:
        return Task(
            config=self.tasks_config['threat_validation_task'],
            agent=self.threat_validation_agent()
        )

    @task
    def threat_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['threat_analysis_task'],
            agent=self.threat_analysis_agent()
        )

    @task
    def knowledge_graph_task(self) -> Task:
        return Task(
            config=self.tasks_config['knowledge_graph_task'],
            agent=self.knowledge_graph_agent()
        )

    @crew
    def crew(self) -> StrikeCrew:
	    """Creates the StrikeCrew crew"""
        return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=2,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)