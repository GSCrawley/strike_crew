# config.py
# from pydantic import BaseModel

from typing import Dict, Any, List, Union

class CrewConfig():
    def __init__(self, agents_config: Dict[str, Any], tasks_config: Dict[str, Any]):
        if 'agents' not in agents_config or 'crew_manager' not in agents_config['agents']:
            raise KeyError("'crew_manager' key not found in agents_config['agents']")
        
        self.crew_manager_config = agents_config['agents']['crew_manager']
        self.agents_config = agents_config
        
        # Ensure tasks are in the correct format
        if 'tasks' in tasks_config:
            if isinstance(tasks_config['tasks'], dict):
                self.tasks_config = tasks_config
                # Ensure each task has all required fields
                for task_name, task_data in self.tasks_config['tasks'].items():
                    if not isinstance(task_data, dict):
                        raise ValueError(f"Task '{task_name}' must be a dictionary")
                    task_data.setdefault('name', task_name)
                    task_data.setdefault('description', 'No description provided')
                    task_data.setdefault('expected_output', 'Task completed successfully')
                    task_data.setdefault('output_json', False)
                    task_data.setdefault('output_file', False)
            else:
                raise ValueError("tasks_config['tasks'] must be a dictionary")
        else:
            raise KeyError("'tasks' key not found in tasks_config")
