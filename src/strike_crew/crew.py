# Strike Crew - copyright (c) 2024 Gideon Shalom Crawley
# crew.py

import os
import re
import json
import uuid
from py2neo import Graph, Node, Relationship
from neo4j import GraphDatabase
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from crewai import Agent, Crew, Process, Task 
from langchain_groq import ChatGroq
# from langchain_openai import ChatOpenAI
from strike_crew.config import CrewConfig
from strike_crew.models import EmergingThreat, IOC, TTP, ThreatActor, CVE, Campaign
from strike_crew.tools.custom_tool import (
    Neo4JSearchTool, WebSearchTool, WebScraperTool, DiffbotNLPTool, DiffbotGraphUpdateTool
)

from dotenv import load_dotenv

load_dotenv()

class UserInput(BaseModel):
    threat_types: List[str]
    sources: List[str]

class StrikeCrew:
    def __init__(self, config: CrewConfig):
        self.config = config
        # self.agents = []
        # self.tasks = []
        # self.crew = None
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
        self.nlp_tool = DiffbotNLPTool()
        self.graph_update_tool = DiffbotGraphUpdateTool(self.neo4j_uri, self.neo4j_user, self.neo4j_password)

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
            # manager_llm=ChatGroq(temperature=0, model_name="llama3-70b-8192"),  
            verbose=True
        )

        Crew.tools = [
            self.web_search_tool,
            self.web_scraper_tool,
            self.neo4j_search_tool,
            self.nlp_tool,
            self.graph_update_tool
        ]
    
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
        
        # Extract the threat name and basic information
        threat_match = re.search(r'\*\*(.*?)\s*Comprehensive Report\*\*(.*?)(?=\n\n)', raw_results, re.DOTALL)
        if threat_match:
            threat_name = threat_match.group(1).strip()
            threat_description = threat_match.group(2).strip()

            # Extract nodes and edges
            nodes = []
            edges = []

            # Extract nodes
            node_matches = re.findall(r'(\d+)\.\s*(.*?)\n((?:\s*-.*\n)*)', raw_results, re.DOTALL)
            for match in node_matches:
                node_name = match[1].strip()
                node_properties = dict(re.findall(r'-\s*(.*?):\s*(.*)', match[2]))
                nodes.append({"name": node_name, "properties": node_properties})

            # Extract edges
            edge_matches = re.findall(r'\((.*?)\)\s*-\[(.*?)\]->\s*\((.*?)\)', raw_results)
            for match in edge_matches:
                edges.append({"from": match[0], "relation": match[1], "to": match[2]})

            emerging_threat = EmergingThreat(
                name=threat_name,
                description=threat_description,
                threat_type=nodes[0]["properties"].get("Type", "Unknown") if nodes else "Unknown",
                iocs=IOC(),  # You might want to extract this from the data if available
                ttps=TTP(),  # You might want to extract this from the data if available
                threat_actors=[],  # You might want to extract this from the data if available
                cves=[],  # You might want to extract this from the data if available
                campaigns=[],  # You might want to extract this from the data if available
                targeted_sectors=[],  # You might want to extract this from the data if available
                targeted_countries=[],  # You might want to extract this from the data if available
                first_seen=datetime.now(),  # You might want to extract this from the data if available
                last_seen=datetime.now(),
                confidence_score=1.0,
                data_sources=[],  # You might want to extract this from the data if available
                mitigation_recommendations=[],  # You might want to extract this from the data if available
                related_threats=[],  # You might want to extract this from the data if available
                tags=[nodes[0]["properties"].get("Category", "Unknown")] if nodes else [],
                references=[],  # You might want to extract this from the data if available
                nodes=nodes,
                edges=edges,
                additional_info={}  # You can add any additional information here
            )
            processed_results.append(emerging_threat)
        
        return processed_results

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
                f.write(f"Type: {threat.threat_type}\n")
                f.write(f"Category: {threat.tags[0] if threat.tags else 'Unknown'}\n")
                f.write(f"First Discovered: {threat.first_seen.year}\n")
                f.write(f"Affected Systems: {', '.join(threat.additional_info['properties'].get('Affected Systems', '').split(', '))}\n")
                f.write("\nRelated Nodes:\n")
                for node in threat.additional_info['related_nodes']:
                    f.write(f"  - {node['name']} ({node['properties']['Type']})\n")
                f.write("\nRelationships:\n")
                for edge in threat.additional_info['edges']:
                    f.write(f"  - ({edge[0]}) -[{edge[1]}]-> ({edge[2]})\n")
                f.write("\n")
        print(f"Threat intelligence report saved to {filename}")

    def _update_neo4j_database(self, results: List[EmergingThreat]) -> str:
            graph_id = str(uuid.uuid4())
            try:
                with GraphDatabase.driver(self.neo4j_uri, auth=(self.neo4j_user, self.neo4j_password)) as driver:
                    with driver.session() as session:
                        for threat in results:
                            session.write_transaction(self._create_threat_node, threat, graph_id)
                        
                        # Verify that nodes were created
                        verification_query = (
                            "MATCH (t:EmergingThreat {graph_id: $graph_id}) "
                            "RETURN count(t) as count"
                        )
                        result = session.run(verification_query, graph_id=graph_id).single()
                        if result and result["count"] > 0:
                            print(f"Successfully added {result['count']} nodes to Neo4j with graph_id: {graph_id}")
                        else:
                            print(f"Warning: No nodes were found with graph_id: {graph_id}")
                
                print("Neo4j database updated with new threat intelligence")
            except Exception as e:
                print(f"Error updating Neo4j database: {e}")
            return graph_id

    @staticmethod
    def _create_threat_node(tx, threat: EmergingThreat, graph_id: str):
        # Create the main threat node
        main_node_query = (
            "CREATE (t:EmergingThreat {name: $name, type: $type, category: $category, "
            "first_discovered: $first_discovered, affected_systems: $affected_systems, "
            "graph_id: $graph_id})"
        )
        tx.run(main_node_query, 
            name=threat.name,
            type=threat.threat_type,
            category=threat.tags[0] if threat.tags else 'Unknown',
            first_discovered=threat.first_seen.year,
            affected_systems=threat.additional_info['properties'].get('Affected Systems', '').split(', '),
            graph_id=graph_id)

        # Create other nodes and relationships
        for node in threat.additional_info['related_nodes']:
            node_query = (
                f"CREATE (n:{node['properties']['Type']} {{name: $name, "
                f"type: $type, graph_id: $graph_id}})"
            )
            tx.run(node_query, 
                name=node['name'],
                type=node['properties']['Type'],
                graph_id=graph_id)

        # Create edges
        for edge in threat.additional_info['edges']:
            edge_query = (
                "MATCH (a {name: $from, graph_id: $graph_id}), "
                "(b {name: $to, graph_id: $graph_id}) "
                "CREATE (a)-[r:$relation]->(b)"
            )
            tx.run(edge_query,
                from_=edge[0],
                relation=edge[1],
                to=edge[2],
                graph_id=graph_id)


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