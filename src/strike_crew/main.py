#!/usr/bin/env python
import sys
import os
from strike_crew.crew import StrikeCrew
import yaml

def load_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_dir = os.path.join(base_dir, 'config')
    agents_config_path = os.path.join(config_dir, 'agents.yaml')
    tasks_config_path = os.path.join(config_dir, 'tasks.yaml')
    
    print(f"Base directory: {base_dir}")
    print(f"Config directory: {config_dir}")
    print(f"Agents config path: {agents_config_path}")
    print(f"Tasks config path: {tasks_config_path}")

    # Load agent and task configurations
    agents_config = load_config(agents_config_path)
    tasks_config = load_config(tasks_config_path)
    
    # Initialize the StrikeCrew with loaded configurations
    strike_crew = StrikeCrew(agents_config=agents_config, tasks_config=tasks_config)
    
    # Kickoff the crew process
    result = strike_crew.kickoff()
    print(result)

if __name__ == "__main__":
    main()
