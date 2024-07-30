from crewai import Agent

class CrewManager(Agent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def plan_tasks(self, objective):
        """Plan tasks based on the given objective."""
        prompt = f"Given the objective: '{objective}', create a plan of tasks to achieve this. Consider the capabilities of the OSINT Analyst, OSINT Scraper, Validation Agent, and Knowledge Graph Agents."
        return self.execute_task(prompt)

    def delegate_task(self, task, agents):
        """Delegate a task to the most suitable agent."""
        prompt = f"Given the task: '{task}', and the available agents: {[agent.name for agent in agents]}, which agent is best suited to perform this task? Explain your reasoning."
        return self.execute_task(prompt)

    def validate_output(self, task, output):
        """Validate the output of a task."""
        prompt = f"Review the output of the task: '{task}'. The output is: '{output}'. Is this output satisfactory? If not, what improvements are needed?"
        return self.execute_task(prompt)

    def execute_task(self, prompt):
        """Execute a task based on the given prompt."""
        return self.run(prompt)