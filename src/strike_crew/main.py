# main.py

from strike_crew.config_loader import load_config
from strike_crew.crew import StrikeCrew
from strike_crew.config import CrewConfig

def main():
    agents_config_path = 'src/strike_crew/config/agents.yaml'
    tasks_config_path = 'src/strike_crew/config/tasks.yaml'
    agents_config = load_config(agents_config_path)
    tasks_config = load_config(tasks_config_path)

    # Create the CrewConfig
    crew_config = CrewConfig(
        agents_config=agents_config, 
        tasks_config=tasks_config
        )

    # Initialize the StrikeCrew
    strike_crew = StrikeCrew(crew_config)

    strike_crew.run()
    # # Run the crew
    # results = strike_crew.run("Latest cybersecurity threats")

    # # Process and print results
    # for result in results:
    #     print(f"Emerging Threat: {result}")

if __name__ == "__main__":
    main()