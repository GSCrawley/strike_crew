# Strike Crew - copyright (c) 2024 Gideon Shalom Crawley
# crew.py
import uuid
from py2neo import Graph, Node, Relationship

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
    Neo4JSearchTool, WebSearchTool, WebScraperTool, NLPTool, GraphUpdateTool
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
        self.neo4j_uri = os.getenv("NEO4J_URI")
        self.neo4j_user = os.getenv("NEO4J_USER")
        self.neo4j_password = os.getenv("NEO4J_PASSWORD")
        self.initialize_tools()
        self.initialize_agents_and_tasks()
        self.graph = Graph(self.neo4j_uri, auth=(self.neo4j_user, self.neo4j_password))

    def initialize_tools(self):
        self.web_search_tool = WebSearchTool(os.getenv("GOOGLE_SERPER_API_KEY"))
        self.web_scraper_tool = WebScraperTool()
        self.neo4j_search_tool = Neo4JSearchTool(self.neo4j_uri, self.neo4j_user, self.neo4j_password)
        self.nlp_tool = NLPTool()
        self.graph_update_tool = GraphUpdateTool(self.neo4j_uri, self.neo4j_user, self.neo4j_password)

    def initialize_agents_and_tasks(self):
    # Define the agents without specific tools or tasks
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
            allow_delegation=False
        )

        self.validation_agent = Agent(
            role="Validation Agent",
            goal="Verify and validate gathered threat intelligence, ensuring accuracy and relevance of collected data",
            backstory="Expert in threat intelligence validation techniques",
            verbose=True,
            allow_delegation=False
        )

        self.knowledge_graph_agent_1 = Agent(
            role="Knowledge Graph Agent 1",
            goal="Extract structured information from unstructured text",
            backstory="Specialized in natural language processing for cybersecurity",
            verbose=True,
            allow_delegation=False
        )

        self.knowledge_graph_agent_2 = Agent(
            role="Knowledge Graph Agent 2",
            goal="Maintain an up-to-date graph database of threat intelligence",
            backstory="Expert in graph databases and threat intelligence structuring",
            verbose=True,
            allow_delegation=False
        )

        self.agents = [
            self.crew_manager,
            self.osint_analyst,
            self.validation_agent,
            self.knowledge_graph_agent_1,
            self.knowledge_graph_agent_2
        ]

        print("Available agents:")
        for agent in self.agents:
            print(f"- {agent.role}")

        # Define tasks without assigning them to specific agents
        self.tasks = [
            Task(
                description="Search for latest cybersecurity threats related to: {initial_query}",
                expected_output="A list of URLs and brief descriptions of recent cybersecurity threats"
            ),
            Task(
                description="Validate and verify the gathered threat intelligence",
                expected_output="A list of verified threat intelligence data, with confidence scores"
            ),
            Task(
                description="Process and analyze the threat intelligence data",
                expected_output="Structured data identifying entities such as threat actors, TTPs, IOCs, and CVEs"
            ),
            Task(
                description="Update the knowledge graph with new threat intelligence",
                expected_output="Confirmation of new nodes and edges added to the Neo4j database, representing the latest threat intelligence"
            ),
            Task(
                description="Generate a summary report of newly discovered threats",
                expected_output="A concise report summarizing new threats, their potential impact, and recommended actions"
            )
        ]

        print("\nDefined tasks:")
        for task in self.tasks:
            print(f"- {task.description}")

        # Create the crew
        self.crew = Crew(
            agents=self.agents,
            tasks=self.tasks,
            manager=self.crew_manager,
            process=Process.hierarchical,
            manager_llm=ChatOpenAI(model="gpt-4"),  
            tools = [
            self.web_search_tool,
            self.web_scraper_tool,
            self.neo4j_search_tool,
            self.nlp_tool,
            self.graph_update_tool
        ],
            verbose=True
        )

        print("\nCrew initialized!")

    def run(self):
        while True:
            user_input = self._get_user_input()
            initial_query = self._generate_initial_query(user_input)
        
            print(f"Generated query: {initial_query}")
        
            emerging_threats = self._create_emerging_threat(initial_query, user_input)
        
            print(f"Number of emerging threats: {len(emerging_threats)}")
        
            if emerging_threats:
                self._save_json_output(emerging_threats)
                self._save_to_file(emerging_threats)
                graph_id = self._update_neo4j_database(emerging_threats)
            
                print(f"New knowledge graph created with ID: {graph_id}")
                print("To view the new knowledge graph, run the following Cypher query in Neo4j Browser:")
                print(f"MATCH (t:EmergingThreat {{graph_id: '{graph_id}'}}) RETURN t")
            else:
                print("No emerging threats were identified in this iteration.")
        
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

    def _create_emerging_threat(self, initial_query: str, user_input: UserInput) -> List[EmergingThreat]:
        raw_results = self.crew.kickoff({"initial_query": initial_query, "user_input": user_input.dict()})
        print(f"Raw results: {raw_results}")  # Debug print
    
        processed_results = self._process_results(raw_results)
    
        if processed_results:
            return processed_results
        else:
            # Create a default EmergingThreat if no results were processed
            return [EmergingThreat(
                name=f"Unknown Threat - {datetime.now()}",
                description=f"No specific threat identified for query: {initial_query}",
                threat_type="Unknown",
                iocs=IOC(),
                ttps=TTP(),
                threat_actors=[],
                cves=[],
                campaigns=[],
                targeted_sectors=[],
                targeted_countries=[],
                first_seen=datetime.now(),
                last_seen=datetime.now(),
                confidence_score=0.0,
                data_sources=[],
                mitigation_recommendations=[],
                related_threats=[],
                tags=[],
                references=[]
            )]

    def _process_results(self, raw_results: str) -> List[EmergingThreat]:
        processed_results = []
        # Split the raw results into individual threat entries
        threat_entries = raw_results.split("\n\n")
    
        for entry in threat_entries:
            if entry.startswith("Threat:"):
                lines = entry.split("\n")
                name = lines[0].replace("Threat:", "").strip()
            
                description = ""
                methodology = ""
                impacts = []
                countermeasures = []
                confidence_score = 0.0
                
                for line in lines[1:]:
                    if line.startswith("- **Methodology**:"):
                        methodology = line.replace("- **Methodology**:", "").strip()
                    elif line.startswith("- **Impacts**:"):
                        impacts = line.replace("- **Impacts**:", "").strip().split(", ")
                    elif line.startswith("- **Countermeasures**:"):
                        countermeasures = line.replace("- **Countermeasures**:", "").strip().split(", ")
                    elif line.startswith("- **Confidence Score**:"):
                        confidence_str = line.replace("- **Confidence Score**:", "").strip()
                        confidence_score = 1.0 if confidence_str == "High" else 0.5 if confidence_str == "Medium" else 0.0
            
                description = f"{methodology}\nImpacts: {', '.join(impacts)}\nCountermeasures: {', '.join(countermeasures)}"
            
                emerging_threat = EmergingThreat(
                    name=name,
                    description=description,
                    threat_type="Relay Attack",
                    iocs=IOC(),  # You might want to extract IOCs from the description if possible
                    ttps=TTP(),  # You might want to extract TTPs from the methodology
                    threat_actors=[],
                    cves=[],
                    campaigns=[],
                    targeted_sectors=[],
                    targeted_countries=[],
                    first_seen=datetime.now(),
                    last_seen=datetime.now(),
                    confidence_score=confidence_score,
                    data_sources=[],
                    mitigation_recommendations=countermeasures,
                    related_threats=[],
                    tags=["Relay Attack"],
                    references=[]
                )
                processed_results.append(emerging_threat)
    
        return processed_results

    def _save_json_output(self, results: List[EmergingThreat]):
            json_data = [result.dict() for result in results]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f'threat_intelligence_output_{timestamp}.json'
            with open(filename, 'w') as f:
                json.dump(json_data, f, indent=2, default=str)
            print(f"JSON output saved to {filename}")

    def _save_to_file(self, results: List[EmergingThreat]):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f'threat_intelligence_report_{timestamp}.txt'
            with open(filename, 'w') as f:
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
            print(f"Threat intelligence report saved to {filename}")

    def _update_neo4j_database(self, results: List[EmergingThreat]) -> str:
        graph_id = str(uuid.uuid4())
        with GraphDatabase.driver(self.neo4j_uri, auth=(self.neo4j_user, self.neo4j_password)) as driver:
            with driver.session() as session:
                for threat in results:
                    session.write_transaction(self._create_threat_node, threat, graph_id)
        print("Neo4j database updated with new threat intelligence")
        return graph_id

    @staticmethod
    def _create_threat_node(tx, threat: EmergingThreat, graph_id: str):
        query = (
            "CREATE (t:EmergingThreat {name: $name, description: $description, threat_type: $threat_type, "
            "first_seen: $first_seen, last_seen: $last_seen, confidence_score: $confidence_score, graph_id: $graph_id}) "
            "WITH t "
            "UNWIND $iocs AS ioc "
            "CREATE (i:IOC {type: ioc.type, value: ioc.value, graph_id: $graph_id}) "
            "CREATE (t)-[:HAS_IOC]->(i) "
            "WITH t "
            "UNWIND $ttps AS ttp "
            "CREATE (p:TTP {type: ttp.type, value: ttp.value, graph_id: $graph_id}) "
            "CREATE (t)-[:USES_TTP]->(p) "
            "WITH t "
            "UNWIND $threat_actors AS actor "
            "CREATE (a:ThreatActor {name: actor.name, description: actor.description, "
            "motivation: actor.motivation, country: actor.country, graph_id: $graph_id}) "
            "CREATE (a)-[:ASSOCIATED_WITH]->(t)"
        )
        tx.run(query, 
               name=threat.name, 
               description=threat.description, 
               threat_type=threat.threat_type,
               first_seen=threat.first_seen, 
               last_seen=threat.last_seen, 
               confidence_score=threat.confidence_score,
               graph_id=graph_id,
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
                },
                "validation_task": {
                    "description": "Validate and verify the gathered threat intelligence",
                },
                "graph_update_task": {
                    "description": "Update the knowledge graph with new threat intelligence",
                }
            }
        }
    )
    strike_crew = StrikeCrew(config)
    strike_crew.run()