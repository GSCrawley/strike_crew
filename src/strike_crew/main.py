#!/usr/bin/env python
import sys
import os
from strike_crew.crew import Crew
from strike_crew.config_loader import load_config
import yaml

def load_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_dir = os.path.join(base_dir, 'config')
    agents_config_path = os.path.join(config_dir, 'agents.yaml')
    tasks_config_path = os.path.join(config_dir, 'tasks.yaml')

    # Load agent and task configurations
    agents_config = load_config(agents_config_path)
    tasks_config = load_config(tasks_config_path)

    # Debug: Print the loaded configurations
    print("Agents Config:", agents_config)
    print("Tasks Config:", tasks_config)
    
    # # Check if 'crew_manager' key exists
    # if 'crew_manager' not in agents_config.get('agents', {}):
    #     print("Error: 'crew_manager' key not found in agents_config['agents']")
    #     sys.exit(1)
    
    #     # Check if 'osint_analyst' key exists within 'agents'
    # if 'osint_analyst' not in agents_config.get('agents', {}):
    #     print("Error: 'osint_analyst' key not found in agents_config['agents']")
    #     sys.exit(1)

    # Initialize the StrikeCrew with loaded configurations
    strike_crew = Crew(agents_config=agents_config, tasks_config=tasks_config)
    
    # Kickoff the crew process
    result = strike_crew.kickoff()
    print(result)

if __name__ == "__main__":
    main()
