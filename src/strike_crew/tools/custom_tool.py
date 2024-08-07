from crewai_tools import BaseTool, Tool
from neo4j import GraphDatabase
from dotenv import load_dotenv
import scrapy
from scrapy.crawler import CrawlerProcess
from typing import List, Dict, Callable
import os
import json 
import re
from datetime import datetime
import pprint
import requests
from urllib.parse import urlparse
from pydantic import PrivateAttr, BaseModel
from bs4 import BeautifulSoup
from langchain_community.graphs import Neo4jGraph
from langchain_experimental.graph_transformers.diffbot import DiffbotGraphTransformer
from langchain_community.utilities.google_serper import GoogleSerperAPIWrapper
from strike_crew.models import EmergingThreat

load_dotenv()

host = "bolt://localhost:7474"
uri = os.getenv('NEO4J_URI')
user = os.getenv('NEO4J_USER')
password = os.getenv('NEO4J_PASSWORD')
nlp = os.getenv('DIFFBOT_NLP_API_TOKEN')
custom_search = os.getenv('GOOGLE_API_KEY')
api_key = os.getenv('SERPER_API_KEY')
search_engine = os.getenv('GOOGLE_CSE_ID')

diffbot_nlp = DiffbotGraphTransformer(nlp)

graph = Neo4jGraph(url=uri, username=user, password=password)


class Neo4jDatabase:
    def __init__(self, host, user, password):
        self.driver = GraphDatabase.driver(host, auth=(user, password))
        self.refresh_schema()

    def close(self):
        self.driver.close()

    def query(self, query, parameters=None):
        with self.driver.session() as session:
            result = session.run(query, parameters)
            return [r.data() for r in result]

    def refresh_schema(self):
        node_properties_query = """
        CALL apoc.meta.data()
        YIELD label, other, elementType, type, property
        WHERE NOT type = "RELATIONSHIP" AND elementType = "node"
        WITH label AS nodeLabels, collect({property:property, type:type}) AS properties
        RETURN {labels: nodeLabels, properties: properties} AS output
        """
        try:
            node_props = [el["output"] for el in self.query(node_properties_query)]
        except Exception as e:
            raise ValueError(f"Failed to refresh schema: {e}")

        rel_properties_query = """
        CALL apoc.meta.data()
        YIELD label, other, elementType, type, property
        WHERE type = "RELATIONSHIP" AND elementType = "relationship"
        WITH label AS relLabels, collect({property:property, type:type}) AS properties
        RETURN {labels: relLabels, properties: properties} AS output
        """
        rel_query = """
        MATCH (n)-[r]->(m)
        RETURN distinct type(r) as output
        """
        
        try:
            rel_props = [el["output"] for el in self.query(rel_properties_query)]
            rels = [el["output"] for el in self.query(rel_query)]
        except Exception as e:
            raise ValueError(f"Failed to refresh relationships: {e}")

        schema = self.schema_text(node_props, rel_props, rels)
        self.schema = schema
        # print(schema)

    def schema_text(self, node_props, rel_props, rels):
        schema = "Node Properties: \n"
        for prop in node_props:
            schema += f"{prop}\n"
        schema += "Relationship Properties: \n"
        for prop in rel_props:
            schema += f"{prop}\n"
        schema += "Relationships: \n"
        for rel in rels:
            schema += f"{rel}\n"
        return schema

class WebSearchTool(BaseTool):
    name: str = "Web Search"
    description: str = "Searches the web for information based on user queries."
    _search: GoogleSerperAPIWrapper = PrivateAttr()  # Use PrivateAttr to exclude from Pydantic validation
    
    def __init__(self, api_key: str):
        super().__init__()
        self._search = GoogleSerperAPIWrapper(api_key=api_key)

    def _run(self, query: str) -> str:
        try:
            results = self._search.run(query)
            return results
        except Exception as e:
            return f"An error occurred: {str(e)}"

class ScrapedThreatInfo(BaseModel):
    name: str = ""
    description: str = ""
    threat_type: str = ""
    iocs: Dict[str, List[str]] = {
        "ip_addresses": [], "domains": [], "urls": [], 
        "file_hashes": [], "email_addresses": []
    }
    ttps: Dict[str, List[str]] = {
        "tactics": [], "techniques": [], "sub_techniques": [], "procedures": []
    }
    threat_actors: List[Dict[str, str]] = []
    cves: List[Dict[str, str]] = []
    campaigns: List[Dict[str, str]] = []
    targeted_sectors: List[str] = []
    targeted_countries: List[str] = []
    first_seen: str = ""
    last_seen: str = ""
    confidence_score: float = 0.0
    data_sources: List[str] = []
    mitigation_recommendations: List[str] = []
    related_threats: List[str] = []
    tags: List[str] = []
    references: List[str] = []

class ThreatSpider(scrapy.Spider):
    name = 'threat_spider'
    
    def __init__(self, url=None, threat_name=None, *args, **kwargs):
        super(ThreatSpider, self).__init__(*args, **kwargs)
        self.start_urls = [url]
        self.threat_name = threat_name
        self.threat_info = ScrapedThreatInfo()

    def parse(self, response):
        self.threat_info.name = self.threat_name or self.extract_text(response, '//h1')
        self.threat_info.description = self.extract_text(response, '//meta[@name="description"]/@content')
        self.threat_info.threat_type = self.extract_text(response, '//p[contains(text(), "Type:")]')
        
        # Extract IOCs
        self.threat_info.iocs["ip_addresses"] = self.extract_patterns(response, r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')
        self.threat_info.iocs["domains"] = self.extract_patterns(response, r'\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}\b')
        self.threat_info.iocs["urls"] = response.xpath('//a/@href').getall()
        self.threat_info.iocs["file_hashes"] = self.extract_patterns(response, r'\b[a-fA-F0-9]{32,64}\b')
        self.threat_info.iocs["email_addresses"] = self.extract_patterns(response, r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        
        # Extract TTPs (simplified, might need refinement)
        ttp_text = self.extract_text(response, '//p[contains(text(), "TTP") or contains(text(), "Tactics, Techniques, and Procedures")]')
        if ttp_text:
            self.threat_info.ttps["tactics"] = [t.strip() for t in ttp_text.split(',') if t.strip()]
        
        # Extract other information (simplified, might need refinement)
        self.threat_info.threat_actors = [{"name": actor.strip()} for actor in self.extract_text(response, '//p[contains(text(), "Threat Actor")]').split(',') if actor.strip()]
        self.threat_info.cves = [{"id": cve.strip()} for cve in re.findall(r'CVE-\d{4}-\d+', response.text)]
        self.threat_info.campaigns = [{"name": campaign.strip()} for campaign in self.extract_text(response, '//p[contains(text(), "Campaign")]').split(',') if campaign.strip()]
        
        self.threat_info.first_seen = self.extract_date(response, 'First Seen')
        self.threat_info.last_seen = self.extract_date(response, 'Last Seen')
        
        self.threat_info.mitigation_recommendations = self.extract_list(response, 'Mitigation')
        self.threat_info.related_threats = self.extract_list(response, 'Related Threats')
        self.threat_info.tags = self.extract_list(response, 'Tags')
        self.threat_info.references = response.xpath('//a[contains(@href, "http")]/@href').getall()

    def extract_text(self, response, xpath):
        return ' '.join(response.xpath(f'{xpath}//text()').getall()).strip()

    def extract_patterns(self, response, pattern):
        return list(set(re.findall(pattern, response.text)))

    def extract_date(self, response, date_type):
        date_text = self.extract_text(response, f'//p[contains(text(), "{date_type}")]')
        try:
            return str(datetime.strptime(date_text, '%Y-%m-%d').date())
        except ValueError:
            return ""

    def extract_list(self, response, list_type):
        list_text = self.extract_text(response, f'//p[contains(text(), "{list_type}")]')
        return [item.strip() for item in list_text.split(',') if item.strip()]

class WebScraperTool(Tool):
    name: str = "Web Scraper"
    description: str = "Scrapes specific threat information from a given URL and returns structured data."

    def __init__(self):
        super().__init__(
            name=self.name,
            description=self.description,
            func=self.run
        )
    
    def run(self, url: str, threat_name: str = "") -> str:
        result = self._run(url, threat_name)
        return json.dumps(result)

    def _run(self, url: str, threat_name: str = "") -> Dict:
        process = CrawlerProcess(settings={
            'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'LOG_LEVEL': 'ERROR'
        })
        spider = ThreatSpider(url=url, threat_name=threat_name)
        process.crawl(spider)
        process.start()
        
        return spider.threat_info.dict()

class NLPTool(Tool):
    name: str = "NLP Tool"
    description: str = "Processes text to extract threat intelligence entities."

    def run(self, content: str) -> str:
        try:
            # Parse the JSON string back into a dictionary
            data = json.loads(content)
            # Process the data to extract entities
            entities = self._extract_entities(data)
            return json.dumps(entities)
        except json.JSONDecodeError:
            # If the input is not JSON, process it as plain text
            entities = self._extract_entities_from_text(content)
            return json.dumps(entities)

    def _extract_entities(self, data: Dict) -> Dict:
        # Extract entities from the structured data
        # This is a simplified example; you'd want to implement more sophisticated entity extraction here
        entities = {
            "threat_name": data.get("name", ""),
            "cves": data.get("iocs", {}).get("cves", []),
            "ttps": data.get("ttps", {}),
            "targeted_systems": data.get("targeted_systems", []),
            "data_sources": data.get("data_sources", [])
        }
        return entities

    def _extract_entities_from_text(self, text: str) -> Dict:
        # Implement text-based entity extraction here
        # This is where you'd use NLP techniques to extract entities from unstructured text
        # For now, we'll just return a placeholder
        return {"extracted_text": text}

class GraphUpdateTool(Tool):
    name: str = "Graph Update Tool"
    description: str = "Creates or updates nodes and edges in the Neo4j graph database."

    def run(self, entities: str) -> str:
        data = json.loads(entities)
        graph_id = self._update_graph(data)
        return json.dumps({"graph_id": graph_id})

    def _update_graph(self, data: Dict) -> str:
        graph_id = str(uuid.uuid4())
        
        with GraphDatabase.driver(self.neo4j_uri, auth=(self.neo4j_user, self.neo4j_password)) as driver:
            with driver.session() as session:
                session.write_transaction(self._create_threat_node, data, graph_id)
        
        return graph_id

    @staticmethod
    def _create_threat_node(tx, data: Dict, graph_id: str):
        query = (
            "CREATE (t:Threat {name: $name, graph_id: $graph_id}) "
            "WITH t "
            "UNWIND $cves AS cve "
            "MERGE (c:CVE {id: cve}) "
            "CREATE (t)-[:HAS_CVE]->(c) "
            "WITH t "
            "UNWIND $ttps AS ttp "
            "MERGE (p:TTP {name: ttp}) "
            "CREATE (t)-[:USES_TTP]->(p) "
            "WITH t "
            "UNWIND $targeted_systems AS system "
            "MERGE (s:System {name: system}) "
            "CREATE (t)-[:TARGETS]->(s) "
            "WITH t "
            "UNWIND $data_sources AS source "
            "MERGE (d:DataSource {name: source}) "
            "CREATE (t)-[:DISCOVERED_BY]->(d)"
        )
        tx.run(query, 
               name=data['threat_name'],
               graph_id=graph_id,
               cves=data['cves'],
               ttps=data['ttps'].get('techniques', []),
               targeted_systems=data['targeted_systems'],
               data_sources=data['data_sources'])
