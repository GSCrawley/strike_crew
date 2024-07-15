#!/usr/bin/env python
import sys
from crew import StrikeCrew
import yaml

def load_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

# Assuming the StrikeCrew class correctly initializes agents and tasks within its constructor or methods
def main():
    # Load agent and task configurations
    agents_config = load_config('config/agents.yaml')
    tasks_config = load_config('config/tasks.yaml')

    # Initialize the StrikeCrew with loaded configurations
    strike_crew = StrikeCrew(agents_config=agents_config, tasks_config=tasks_config)

    # Kickoff the crew process
    result = strike_crew.kickoff()
    print(result)

if __name__ == "__main__":
    main()
