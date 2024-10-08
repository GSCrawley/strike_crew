# Strike Crew - copyright (c) 2024 Gideon Shalom Crawley
# crew.py
import time
import logging
from functools import wraps
import os
import re
import json
import uuid
from py2neo import Graph, Node, Relationship
from neo4j import GraphDatabase
from datetime import datetime
from typing import List, Dict, Any, Optional, Mapping, Type, Callable
from pydantic import BaseModel, Field
from crewai import Agent, Crew, Process, Task
from langchain_groq import ChatGroq
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langchain_core.outputs import ChatResult, ChatGeneration
from strike_crew.llm import CustomGroqLLM
# from langchain_openai import ChatOpenAI
from strike_crew.config import CrewConfig, GroqLLMConfig
from strike_crew.models import EmergingThreat, IOC, TTP, ThreatActor, CVE, Campaign
from strike_crew.tools.custom_tool import (
    WebSearchTool, WebScraperTool, NLPTool, GraphUpdateTool
)
from langchain_experimental.graph_transformers.diffbot import DiffbotGraphTransformer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from dotenv import load_dotenv

load_dotenv()

nlp = os.getenv('DIFFBOT_NLP_API_TOKEN')
diffbot_nlp = DiffbotGraphTransformer(nlp)

class UserInput(BaseModel):
    threat_types: List[str]
    sources: List[str]

class StrikeCrew:
    def __init__(self, config: CrewConfig):
        self.config = config
        self.groq_llm_config = GroqLLMConfig(
            temperature=config.llm_config.temperature,
            model_name=config.llm_config.model_name
        )
        self.llm = CustomGroqLLM(config.get_llm_config())
        # self.agents = []
        # self.tasks = []
        # self.crew = None
        self.neo4j_uri = os.getenv("NEO4J_URI")
        self.neo4j_user = os.getenv("NEO4J_USER")
        self.neo4j_password = os.getenv("NEO4J_PASSWORD")
        self.initialize_tools()
        # self.initialize_agents_and_tasks()
        self.graph = Graph(self.neo4j_uri, auth=(self.neo4j_user, self.neo4j_password))
        # self.groq_llm = ChatGroq(temperature=0, model_name="mixtral-8x7b-32768")
        self.api_call_count = 0
        self.last_api_call = 0

    def initialize_tools(self):
        self.web_search_tool = WebSearchTool(os.getenv("SERPAPI_API_KEY"))
        self.web_scraper_tool = WebScraperTool()
        # self.neo4j_search_tool = Neo4JSearchTool(self.neo4j_uri, self.neo4j_user, self.neo4j_password)
        
        self.nlp_tool = NLPTool()
        self.graph_update_tool = GraphUpdateTool(
                        neo4j_uri=self.neo4j_uri,
                        neo4j_user=self.neo4j_user,
                        neo4j_password=self.neo4j_password
        )

    # def groq_llm(self):
    #     return CustomGroqLLM()

    def osint_analyst(self) -> Agent:
        return Agent(
            role="OSINT Analyst",
            goal="Find relevant and recent cybersecurity threat data",
            backstory="Expert in open-source intelligence gathering",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[self.web_search_tool, self.web_scraper_tool, self.nlp_tool]
        )

    def data_scraper(self) -> Agent:
        return Agent(
            role="Data Scraper",
            goal="Scrape and extract threat intelligence data",
            backstory="Expert in data scraping and extraction techniques",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[self.web_search_tool, self.web_scraper_tool]
        )

    def validation_agent(self) -> Agent:
        return Agent(
            role="Validation Agent",
            goal="Verify and validate gathered threat intelligence, ensuring accuracy and relevance of collected data",
            backstory="Expert in threat intelligence validation techniques",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[self.web_search_tool, self.nlp_tool]
        )

    def knowledge_graph_agent(self) -> Agent:
        return Agent(
            role="Knowledge Graph Agent",
            goal="Extract structured information and update threat intelligence graphs",
            backstory="Specialized in natural language processing and graph databases for cybersecurity",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[self.nlp_tool, self.graph_update_tool]
        )

    def database_init_agent(self) -> Agent:
        return Agent(
            role="Database Schema Initializer",
            goal="Ensure the Neo4J database has the correct schema for threat intelligence",
            backstory="You are a database expert specializing in graph databases for cybersecurity",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[self.nlp_tool, self.graph_update_tool]
        )

    def search_task(self, initial_query: str, sources: List[str]) -> Task:
        return Task(
            description=f"Search for latest cybersecurity threats related to: {initial_query}. "
                        f"Only use the following sources: {', '.join(sources)}",
            expected_output="A comprehensive list of recent cybersecurity threats related to the query, "
                            "including threat names, descriptions, IOCs, and other relevant details.",
            agent=self.osint_analyst()
        )
    
    def data_extraction_task(self) -> Task:
        return Task(
            description="Extract threat intelligence data from the search results.",
            expected_output="A list of threat intelligence data in str format, with confidence scores and any discrepancies noted.",
            agent=self.data_scraper()
        )
    
    # def extract_iocs_task(self) -> Task:
    #     return Task(
    #         description="Identify and extract Indicators of Compromise (IOCs) from the threat intelligence data.",
    #         expected_output="A list of IOCs in str format, with confidence scores and any discrepancies noted.",
    #         agent=self.data_scraper()
    #     )
    
    def validation_task(self) -> Task:
        return Task(
            description="Validate and verify the gathered threat intelligence. Ensure all information aligns with the EmergingThreat schema.",
            expected_output="A validated list of threat intelligence data in json format, with confidence scores and any discrepancies noted.",
            agent=self.validation_agent()
        )

    # def validate_iocs_task(self) -> Task:
    #     return Task(
    #         description="Validate and verify the gathered threat intelligence. Ensure all information aligns with the EmergingThreat schema.",
    #         expected_output="A validated list of threat intelligence data in json format, with confidence scores and any discrepancies noted.",
    #         agent=self.validation_agent()
    #     )

    def knowledge_graph_task(self) -> Task:
        return Task(
            description="Parse the validated threat information into Entities, Attributes, and Relationships. "
                        "Create a Neo4j knowledge graph using this structured data. "
                        "Ensure all fields in the EmergingThreat schema are populated.",
            expected_output="A confirmation of the created Neo4j knowledge graph, including the graph ID and a summary of nodes and relationships created.",
            agent=self.knowledge_graph_agent()
        )

    def rate_limit(max_per_minute):
        min_interval = 60.0 / max_per_minute
        def decorator(func):
            last_called = [0.0]
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                elapsed = time.time() - last_called[0]
                left_to_wait = min_interval - elapsed
                if left_to_wait > 0:
                    time.sleep(left_to_wait)
                ret = func(self, *args, **kwargs)
                last_called[0] = time.time()
                return ret
            return wrapper
        return decorator

    # Then apply it to methods that make API calls, e.g.:
    @rate_limit(max_per_minute=10)
    def run(self):
        while True:
            user_input = self._get_user_input()
            initial_query = self._generate_initial_query(user_input)
            
            print(f"Generated query: {initial_query}")
            
            crew = Crew(
                agents=[self.osint_analyst(), self.data_scraper(), self.validation_agent(), self.knowledge_graph_agent(), self.database_init_agent()],
                tasks=[
                    self.search_task(initial_query, user_input.sources),
                    self.validation_task(),
                    self.data_extraction_task(),
                    # self.extract_iocs_task(),
                    # self.validate_iocs_task(),
                    self.knowledge_graph_task()
                ],
                process=Process.sequential,
                verbose=True
            )

            result = crew.kickoff()
            processed_results = self._process_results(result)
            
            if processed_results:
                self._save_json_output(processed_results)
                self._save_to_file(processed_results)
                graph_id = self._update_neo4j_database(processed_results)
                
                print(f"New knowledge graph created with ID: {graph_id}")
                print("To view the new knowledge graph, run the following Cypher query in Neo4j Browser:")
                print(f"MATCH (n {{graph_id: '{graph_id}'}}) RETURN n")
            else:
                print("No emerging threats were identified in this iteration.")
            
            if not self._should_continue():
                break
    
    def execute_tool_with_fallback(self, primary_tool, fallback_tool, input_data):
        try:
            result = primary_tool.run(input_data)
            return result
        except Exception as e:
            print(f"Primary tool failed: {e}. Attempting fallback.")
            return fallback_tool.run(input_data)
            
    def _get_user_input(self) -> UserInput:
        threat_types = input("Enter specific types of threats you're interested in (comma-separated, or press Enter for all): ").split(',')
        threat_types = [t.strip() for t in threat_types if t.strip()]
        
        sources = input("Enter specific sources you'd like searched (comma-separated): ").split(',')
        sources = [s.strip() for s in sources if s.strip()]
        
        return UserInput(threat_types=threat_types, sources=sources)

    def _generate_initial_query(self, user_input: UserInput) -> str:
        query_parts = ["Latest cybersecurity threats"]
        
        if user_input.threat_types:
            query_parts.append(f"related to {', '.join(user_input.threat_types)}")
        
        return " ".join(query_parts)

    def _process_results(self, raw_results: str) -> List[EmergingThreat]:
        processed_results = []
        current_threat = None
        current_section = None

        for line in raw_results.split('\n'):
            if line.startswith("* Threat:"):
                if current_threat:
                    processed_results.append(current_threat)
                current_threat = EmergingThreat(
                    name=line.split(":")[1].strip(),
                    entities=[],
                    relationships=[]
                )
            elif '* Entities:' in line:
                current_section = 'entities'
            elif '* Relationships:' in line:
                current_section = 'relationships'
            elif current_section == 'entities' and line.strip().startswith('+'):
                entity = self._parse_entity(line)
                if entity and current_threat:
                    current_threat.entities.append(entity)
            elif current_section == 'relationships' and line.strip().startswith('+'):
                relationship = self._parse_relationship(line)
                if relationship and current_threat:
                    current_threat.relationships.append(relationship)

        if current_threat:
            processed_results.append(current_threat)

        return processed_results

    def _parse_entity(self, line: str) -> Dict:
        match = re.match(r'\+\s+(.+?):\s+(.+)', line.strip())
        if match:
            name, entity_type = match.groups()
            return {'name': name.strip(), 'type': entity_type.strip()}
        return {}

    def _parse_relationship(self, line: str) -> Dict:
        match = re.match(r'\+\s+(.+?)\s+-\s+(.+?)\s+-\s+(.+)', line.strip())
        if match:
            source, rel_type, target = match.groups()
            return {'source': source.strip(), 'type': rel_type.strip(), 'target': target.strip()}
        return {}
   
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

    @staticmethod
    def _create_threat_node(tx, threat: EmergingThreat, graph_id: str):
        # Create the main EmergingThreat node
        main_node_query = (
            "CREATE (t:EmergingThreat {name: $name, description: $description, threat_type: $threat_type, "
            "first_seen: $first_seen, last_seen: $last_seen, confidence_score: $confidence_score, graph_id: $graph_id})"
        )
        tx.run(main_node_query, 
            name=threat.name,
            description=threat.description,
            threat_type=threat.threat_type,
            first_seen=threat.first_seen,
            last_seen=threat.last_seen,
            confidence_score=threat.confidence_score,
            graph_id=graph_id
        )

        # Create IOC nodes
        for ioc_type, iocs in threat.iocs.dict().items():
            for ioc in iocs:
                tx.run(
                    "MATCH (t:EmergingThreat {graph_id: $graph_id}) "
                    "CREATE (i:IOC {type: $type, value: $value, graph_id: $graph_id}) "
                    "CREATE (t)-[:HAS_IOC]->(i)",
                    graph_id=graph_id, type=ioc_type, value=ioc
                )

        # Create TTP nodes
        for ttp_type, ttps in threat.ttps.dict().items():
            for ttp in ttps:
                tx.run(
                    "MATCH (t:EmergingThreat {graph_id: $graph_id}) "
                    "CREATE (p:TTP {type: $type, value: $value, graph_id: $graph_id}) "
                    "CREATE (t)-[:USES_TTP]->(p)",
                    graph_id=graph_id, type=ttp_type, value=ttp
                )

        # Create ThreatActor nodes
        for actor in threat.threat_actors:
            tx.run(
                "MATCH (t:EmergingThreat {graph_id: $graph_id}) "
                "CREATE (a:ThreatActor {name: $name, description: $description, motivation: $motivation, country: $country, graph_id: $graph_id}) "
                "CREATE (a)-[:ASSOCIATED_WITH]->(t)",
                graph_id=graph_id, **actor.dict()
            )

        # Create CVE nodes
        for cve in threat.cves:
            tx.run(
                "MATCH (t:EmergingThreat {graph_id: $graph_id}) "
                "CREATE (c:CVE {id: $id, description: $description, severity: $severity, published_date: $published_date, graph_id: $graph_id}) "
                "CREATE (t)-[:EXPLOITS]->(c)",
                graph_id=graph_id, **cve.dict()
            )

        # Create Campaign nodes
        for campaign in threat.campaigns:
            tx.run(
                "MATCH (t:EmergingThreat {graph_id: $graph_id}) "
                "CREATE (c:Campaign {name: $name, description: $description, start_date: $start_date, end_date: $end_date, graph_id: $graph_id}) "
                "CREATE (t)-[:PART_OF]->(c)",
                graph_id=graph_id, **campaign.dict()
            )

        # Create additional nodes and edges as defined by the knowledge graph agent
        for node in threat.nodes:
            tx.run(
                f"CREATE (n:{node['label']} $properties)",
                properties={**node['properties'], 'graph_id': graph_id}
            )

        for edge in threat.edges:
            tx.run(
                "MATCH (s {name: $source, graph_id: $graph_id}) "
                "MATCH (t {name: $target, graph_id: $graph_id}) "
                "CREATE (s)-[r:$type $properties]->(t)",
                source=edge['source'],
                target=edge['target'],
                type=edge['type'],
                properties=edge.get('properties', {}),
                graph_id=graph_id
            )

    def _should_continue(self) -> bool:
            response = input("Would you like to search for another emerging threat? (y/n): ").lower()
            return response == 'y'        


if __name__ == "__main__":
    strike_crew = StrikeCrew(config)
    strike_crew.run()