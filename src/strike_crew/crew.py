# crew.py

import json
from neo4j import GraphDatabase
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from crewai import Agent, Crew, Process, Task
from langchain_openai import ChatOpenAI
from strike_crew.config import CrewConfig
from strike_crew.models import EmergingThreat, IOC, TTP, ThreatActor, CVE, Campaign
from strike_crew.tools.custom_tool import (
    Neo4JSearchTool, WebSearchTool, WebScraperTool,
    DiffbotNLPTool, DiffbotGraphUpdateTool
)
import os
from dotenv import load_dotenv

load_dotenv()

class UserInput(BaseModel):
    threat_types: List[str]
    sources: List[str]

class StrikeCrew:
    def __init__(self, config: CrewConfig):
        self.config = config
        self.agents = []
        self.tasks = []
        self.crew = None
        self.neo4j_uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.neo4j_user = os.getenv("NEO4J_USER", "neo4j")
        self.neo4j_password = os.getenv("NEO4J_PASSWORD", "password")
        self.initialize_agents_and_tasks()

    def initialize_agents_and_tasks(self):
        api_key = os.getenv("GOOGLE_SERPER_API_KEY")
        
        web_search_tool = WebSearchTool(api_key)
        web_scraper_tool = WebScraperTool()
        neo4j_search_tool = Neo4JSearchTool(self.neo4j_uri, self.neo4j_user, self.neo4j_password)
        diffbot_nlp_tool = DiffbotNLPTool()
        diffbot_graph_update_tool = DiffbotGraphUpdateTool(self.neo4j_uri, self.neo4j_user, self.neo4j_password)

        self.crew_manager = Agent(
            role="Crew Manager",
            goal="Orchestrate the threat intelligence gathering process",
            backstory="Expert in managing AI agent teams and coordinating complex cybersecurity workflows",
            verbose=True,
            allow_delegation=True
        )

        self.osint_analyst = Agent(
            role="OSINT Analyst",
            goal="Find relevant and recent cybersecurity threat data",
            backstory="Expert in open-source intelligence gathering",
            verbose=True,
            allow_delegation=False,
            tools=[web_search_tool, web_scraper_tool, neo4j_search_tool]
        )

        self.osint_scraper = Agent(
            role="OSINT Scraper",
            goal="Gather detailed threat data from identified sources",
            backstory="Specialized in web scraping and data extraction",
            verbose=True,
            allow_delegation=False,
            tools=[web_scraper_tool, neo4j_search_tool]
        )

        self.validation_agent = Agent(
            role="Validation Agent",
            goal="Ensure accuracy and relevance of collected data",
            backstory="Expert in threat intelligence validation techniques",
            verbose=True,
            allow_delegation=False,
            tools=[neo4j_search_tool, diffbot_nlp_tool]
        )

        self.knowledge_graph_agent_1 = Agent(
            role="Knowledge Graph Agent 1",
            goal="Process and analyze threat intelligence data",
            backstory="Specialized in natural language processing for cybersecurity",
            verbose=True,
            allow_delegation=False,
            tools=[diffbot_nlp_tool, neo4j_search_tool]
        )

        self.knowledge_graph_agent_2 = Agent(
            role="Knowledge Graph Agent 2",
            goal="Create and update threat intelligence knowledge graphs",
            backstory="Expert in graph databases and threat intelligence structuring",
            verbose=True,
            allow_delegation=False,
            tools=[diffbot_graph_update_tool, neo4j_search_tool]
        )

        self.agents = [
            self.crew_manager,
            self.osint_analyst,
            self.osint_scraper,
            self.validation_agent,
            self.knowledge_graph_agent_1,
            self.knowledge_graph_agent_2
        ]

        self.tasks = [
            Task(
                description=task['description'],
                agent=next(agent for agent in self.agents if agent.name == task['agent'])
            )
            for task in self.config.tasks_config['tasks'].values()
        ]

        self.crew = Crew(
            agents=self.agents,
            tasks=self.tasks,
            manager=self.crew_manager,
            process=Process.hierarchical,
            manager_llm=ChatOpenAI(model="gpt-4"),
            verbose=True
        )

    def run(self):
        while True:
            user_input = self._get_user_input()
            initial_query = self._generate_initial_query(user_input)
            
            emerging_threat = self._create_emerging_threat(initial_query, user_input)
            
            if emerging_threat:
                self._save_json_output([emerging_threat])
                self._save_to_file([emerging_threat])
                self._update_neo4j_database([emerging_threat])
                
                print(f"New EmergingThreats knowledge graph created for: {emerging_threat.name}")
                print("To view the new knowledge graph, run the following Cypher query in Neo4j Browser:")
                print(f"MATCH (t:EmergingThreat {{name: '{emerging_threat.name}'}}) RETURN t")
                
                if not self._should_continue():
                    break
            else:
                print("No new emerging threat was identified in this iteration.")
                if not self._should_continue():
                    break

    def _get_user_input(self) -> UserInput:
        threat_types = input("Enter specific types of threats you're interested in (comma-separated, or press Enter for all): ").split(',')
        threat_types = [t.strip() for t in threat_types if t.strip()]
        
        sources = input("Enter specific sources you'd like searched (comma-separated, or press Enter for all): ").split(',')
        sources = [s.strip() for s in sources if s.strip()]
        
        return UserInput(threat_types=threat_types, sources=sources)

    def _generate_initial_query(self, user_input: UserInput) -> str:
        query_parts = ["Latest cybersecurity threats"]
        
        if user_input.threat_types:
            query_parts.append(f"related to {', '.join(user_input.threat_types)}")
        
        if user_input.sources:
            query_parts.append(f"from {', '.join(user_input.sources)}")
        
        return " ".join(query_parts)

    def _create_emerging_threat(self, initial_query: str, user_input: UserInput) -> Optional[EmergingThreat]:
        raw_results = self.crew.kickoff({"initial_query": initial_query, "user_input": user_input.dict()})
        processed_results = self._process_results(raw_results)
        
        if processed_results:
            return processed_results[0]  # Return the first (and only) EmergingThreat
        return None

    def _process_results(self, raw_results: dict) -> List[EmergingThreat]:
        # This is a simplified example. You'll need to adapt this based on the actual structure of raw_results
        processed_results = []
        if isinstance(raw_results, dict) and 'threat' in raw_results:
            threat_data = raw_results['threat']
            emerging_threat = EmergingThreat(
                name=threat_data.get('name', 'Unknown Threat'),
                description=threat_data.get('description', ''),
                threat_type=threat_data.get('threat_type', 'Unknown'),
                iocs=IOC(**threat_data.get('iocs', {})),
                ttps=TTP(**threat_data.get('ttps', {})),
                threat_actors=[ThreatActor(**actor) for actor in threat_data.get('threat_actors', [])],
                cves=[CVE(**cve) for cve in threat_data.get('cves', [])],
                campaigns=[Campaign(**campaign) for campaign in threat_data.get('campaigns', [])],
                targeted_sectors=threat_data.get('targeted_sectors', []),
                targeted_countries=threat_data.get('targeted_countries', []),
                first_seen=threat_data.get('first_seen'),
                last_seen=threat_data.get('last_seen'),
                confidence_score=threat_data.get('confidence_score', 0.0),
                data_sources=threat_data.get('data_sources', []),
                mitigation_recommendations=threat_data.get('mitigation_recommendations', []),
                related_threats=threat_data.get('related_threats', []),
                tags=threat_data.get('tags', []),
                references=threat_data.get('references', [])
            )
            processed_results.append(emerging_threat)
        return processed_results

    def _save_json_output(self, results: List[EmergingThreat]):
        json_data = [result.dict() for result in results]
        with open('threat_intelligence_output.json', 'w') as f:
            json.dump(json_data, f, indent=2, default=str)
        print("JSON output saved to threat_intelligence_output.json")

    def _save_to_file(self, results: List[EmergingThreat]):
        with open('threat_intelligence_report.txt', 'w') as f:
            for threat in results:
                f.write(f"Threat: {threat.name}\n")
                f.write(f"Description: {threat.description}\n")
                f.write(f"Type: {threat.threat_type}\n")
                f.write("IOCs:\n")
                for ioc_type, iocs in threat.iocs.dict().items():
                    f.write(f"  {ioc_type}: {', '.join(iocs)}\n")
                f.write("TTPs:\n")
                for ttp_type, ttps in threat.ttps.dict().items():
                    f.write(f"  {ttp_type}: {', '.join(ttps)}\n")
                f.write("Threat Actors:\n")
                for actor in threat.threat_actors:
                    f.write(f"  {actor.name}\n")
                f.write("\n")
        print("Threat intelligence report saved to threat_intelligence_report.txt")

    def _update_neo4j_database(self, results: List[EmergingThreat]):
        with GraphDatabase.driver(self.neo4j_uri, auth=(self.neo4j_user, self.neo4j_password)) as driver:
            with driver.session() as session:
                for threat in results:
                    session.write_transaction(self._create_threat_node, threat)
        print("Neo4j database updated with new threat intelligence")

    @staticmethod
    def _create_threat_node(tx, threat: EmergingThreat):
        query = (
            "CREATE (t:EmergingThreat {name: $name, description: $description, threat_type: $threat_type, "
            "first_seen: $first_seen, last_seen: $last_seen, confidence_score: $confidence_score}) "
            "WITH t "
            "UNWIND $iocs AS ioc "
            "CREATE (i:IOC {type: ioc.type, value: ioc.value}) "
            "CREATE (t)-[:HAS_IOC]->(i) "
            "WITH t "
            "UNWIND $ttps AS ttp "
            "CREATE (p:TTP {type: ttp.type, value: ttp.value}) "
            "CREATE (t)-[:USES_TTP]->(p) "
            "WITH t "
            "UNWIND $threat_actors AS actor "
            "MERGE (a:ThreatActor {name: actor.name}) "
            "ON CREATE SET a.description = actor.description, a.motivation = actor.motivation, a.country = actor.country "
            "CREATE (a)-[:ASSOCIATED_WITH]->(t)"
        )
        tx.run(query, name=threat.name, description=threat.description, threat_type=threat.threat_type,
               first_seen=threat.first_seen, last_seen=threat.last_seen, confidence_score=threat.confidence_score,
               iocs=[{"type": k, "value": v} for k, v in threat.iocs.dict().items() if v],
               ttps=[{"type": k, "value": v} for k, v in threat.ttps.dict().items() if v],
               threat_actors=[actor.dict() for actor in threat.threat_actors])

    def _should_continue(self) -> bool:
        response = input("Would you like to search for another emerging threat? (y/n): ").lower()
        return response == 'y'

if __name__ == "__main__":
    config = CrewConfig(
        agents_config={
            "agents": {
                "crew_manager": {
                    "name": "Crew Manager",
                    "role": "Manage and coordinate all other agents",
                    "goal": "Orchestrate the threat intelligence gathering process",
                    "backstory": "Expert in managing AI agent teams and coordinating complex cybersecurity workflows"
                }
            }
        },
        tasks_config={
            "tasks": {
                "search_task": {
                    "description": "Search for latest cybersecurity threats",
                    "agent": "OSINT Analyst"
                },
                "validation_task": {
                    "description": "Validate and verify the gathered threat intelligence",
                    "agent": "Validation Agent"
                },
                "graph_update_task": {
                    "description": "Update the knowledge graph with new threat intelligence",
                    "agent": "Knowledge Graph Agent"
                }
            }
        }
    )
    strike_crew = StrikeCrew(config)
    strike_crew.run()