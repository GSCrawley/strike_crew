from strike_crew.config_loader import load_config
from strike_crew.crew import StrikeCrew
from strike_crew.config import CrewConfig, GroqLLMConfig

def main():
    agents_config_path = 'src/strike_crew/config/agents.yaml'
    tasks_config_path = 'src/strike_crew/config/tasks.yaml'
    agents_config = load_config(agents_config_path)
    tasks_config = load_config(tasks_config_path)
    llm_config = GroqLLMConfig(
        temperature=0,
        model_name="llama-3.1-70b-versatile"
    )

    config = CrewConfig(
        agents_config=agents_config,
        tasks_config=tasks_config,
        llm_config=llm_config
    )

    strike_crew = StrikeCrew(config)
    strike_crew.run()

if __name__ == "__main__":
    main()
