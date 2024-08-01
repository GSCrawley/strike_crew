# Strike Crew - copyright (c) 2024 Gideon Shalom Crawley
# main.py

from strike_crew.config_loader import load_config
from strike_crew.crew import StrikeCrew
from strike_crew.config import CrewConfig

def main():
    agents_config_path = 'src/strike_crew/config/agents.yaml'
    tasks_config_path = 'src/strike_crew/config/tasks.yaml'
    agents_config = load_config(agents_config_path)
    tasks_config = load_config(tasks_config_path)

    crew_config = CrewConfig(
        agents_config=agents_config, 
        tasks_config=tasks_config
        )

    strike_crew = StrikeCrew(crew_config)

    strike_crew.run()

if __name__ == "__main__":
    main()