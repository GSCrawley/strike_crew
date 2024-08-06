# config.py
import yaml
from typing import Dict, Any, List

class CrewConfig:
    def __init__(self, agents_config: Dict[str, Any], tasks_config: Dict[str, Any]):
        self.agents_config = self._validate_agents_config(agents_config)
        self.tasks_config = self._validate_tasks_config(tasks_config)

    def _validate_agents_config(self, agents_config: Dict[str, Any]) -> Dict[str, Any]:
        if 'agents' not in agents_config:
            raise KeyError("'agents' key not found in agents config")
        
        for agent_name, agent_data in agents_config['agents'].items():
            if not isinstance(agent_data, dict):
                raise ValueError(f"Agent '{agent_name}' must be a dictionary")
            agent_data.setdefault('name', agent_name)
            agent_data.setdefault('role', 'No role provided')
            agent_data.setdefault('goal', 'No goal provided')
            agent_data.setdefault('backstory', 'No backstory provided')
            agent_data.setdefault('verbose', True)
            agent_data.setdefault('allow_delegation', True)
            agent_data.setdefault('tools', [])

        return agents_config

    def _validate_tasks_config(self, tasks_config: Dict[str, Any]) -> Dict[str, Any]:
        if 'tasks' not in tasks_config:
            raise KeyError("'tasks' key not found in tasks config")
        
        if not isinstance(tasks_config['tasks'], dict):
            raise ValueError("tasks_config['tasks'] must be a dictionary")
        
        for task_name, task_data in tasks_config['tasks'].items():
            if not isinstance(task_data, dict):
                raise ValueError(f"Task '{task_name}' must be a dictionary")
            task_data.setdefault('name', task_name)
            task_data.setdefault('description', 'No description provided')
            task_data.setdefault('expected_output', 'Task completed successfully')
            task_data.setdefault('agent', 'No agent specified')

        return tasks_config

    # ... (rest of the methods remain the same)