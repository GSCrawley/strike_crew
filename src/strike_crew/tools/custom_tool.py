# from crewai_tools import BaseTool
from langchain.tools import Tool, BaseTool
from neo4j import GraphDatabase
from dotenv import load_dotenv
from scrapy import Spider, Request, signals
from scrapy.crawler import CrawlerProcess
from typing import List, Dict, Callable, Any, Optional, Type
from twisted.internet import reactor
from scrapy.utils.project import get_project_settings
import os
import json 
import re
import uuid
from diffbot import DiffbotClient  # Make sure to import this at the top of your file

from datetime import datetime
import pprint
import requests
from urllib.parse import urlparse
from pydantic import PrivateAttr, BaseModel, Field
from bs4 import BeautifulSoup
from langchain_community.graphs import Neo4jGraph
from langchain_experimental.graph_transformers.diffbot import DiffbotGraphTransformer
from langchain_community.utilities import SerpAPIWrapper
from strike_crew.models import EmergingThreat

load_dotenv()

host = "bolt://localhost:7474"
uri = os.getenv('NEO4J_URI')
user = os.getenv('NEO4J_USER')
password = os.getenv('NEO4J_PASSWORD')
nlp = os.getenv('DIFFBOT_NLP_API_TOKEN')
custom_search = os.getenv('GOOGLE_API_KEY')
api_key = os.getenv('SERPAPI_API_KEY')
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
    description: str = "Searches the web for information based on user queries, using SerpAPI."
    search: SerpAPIWrapper = Field(default_factory=SerpAPIWrapper) 
    
    def __init__(self, api_key: str, **kwargs):
        super().__init__(**kwargs)
        self.search = SerpAPIWrapper()

    def _run(self, query: str) -> str:
        try:
            results = self.search.run(query)
            return results
        except Exception as e:
            return f"An error occurred: {str(e)}"
    
    async def _arun(self, query: str) -> str:
        # Implement async version if needed
        return self._run(query)
    

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

class ThreatSpider(Spider):
    name = 'threat_spider'
    
    def __init__(self, url, threat_name, *args, **kwargs):
        super(ThreatSpider, self).__init__(*args, **kwargs)
        self.start_urls = [url]
        self.threat_name = threat_name
        self.threat_info = {}

    def parse(self, response):
        self.threat_info['name'] = self.threat_name or response.css('h1::text').get()
        self.threat_info['description'] = response.css('meta[name="description"]::attr(content)').get()
        self.threat_info['threat_type'] = response.xpath('//p[contains(text(), "Type:")]//text()').get()

        # Extract IOCs
        self.threat_info['iocs'] = {
            'ip_addresses': response.xpath('//text()').re(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'),
            'domains': response.xpath('//text()').re(r'\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}\b'),
            'urls': response.css('a::attr(href)').getall(),
            'file_hashes': response.xpath('//text()').re(r'\b[a-fA-F0-9]{32,64}\b'),
            'email_addresses': response.xpath('//text()').re(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        }
        
        # Extract TTPs
        self.threat_info['ttps'] = response.xpath('//p[contains(text(), "TTP") or contains(text(), "Tactics, Techniques, and Procedures")]//text()').getall()
        
        # Extract threat actors
        self.threat_info['threat_actors'] = [{"name": actor.strip()} for actor in self.extract_text(response, '//p[contains(text(), "Threat Actor")]').split(',') if actor.strip()]
        
        # Extract CVEs
        self.threat_info['cves'] = [{"id": cve.strip()} for cve in re.findall(r'CVE-\d{4}-\d+', response.text)]
        
        # Extract campaigns
        self.threat_info['campaigns'] = [{"name": campaign.strip()} for campaign in self.extract_text(response, '//p[contains(text(), "Campaign")]').split(',') if campaign.strip()]
        
        # Extract dates
        self.threat_info['first_seen'] = self.extract_date(response, 'First Seen')
        self.threat_info['last_seen'] = self.extract_date(response, 'Last Seen')
        
        # Extract additional information
        self.threat_info['mitigation_recommendations'] = self.extract_list(response, 'Mitigation')
        self.threat_info['related_threats'] = self.extract_list(response, 'Related Threats')
        self.threat_info['tags'] = self.extract_list(response, 'Tags')
        self.threat_info['references'] = response.xpath('//a[contains(@href, "http")]/@href').getall()

        yield self.threat_info

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

class WebScraperInput(BaseModel):
     query: str = Field(..., description="The URL to scrape for threat information")

class WebScraperTool(BaseTool):
    name: str = Field(default="Web Scraper")
    description: str = Field(default="A tool for scraping web content.")
    args_schema:Type[BaseModel] = Field(default=WebScraperInput)

    def __init__(self, **data):
        super().__init__(**data)

    def _run(self, url: str, threat_name: Optional[str] = None) -> str:
        process = CrawlerProcess(settings={
            'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'LOG_LEVEL': 'ERROR'
        })
        results = []

        def crawler_results(item, response, spider):
            results.append(item)

        process.crawl(ThreatSpider, url=url, threat_name=threat_name)
        process.signals.connect(crawler_results, signal=signals.item_scraped)

        process.start()

        if results:
            return json.dumps(results[0], default=str)
        else:
            return json.dumps({"error": "No data scraped"})

# class WebScraperSchema(BaseModel):
#     url: str = Field(..., description="The URL to scrape for threat information")
#     threat_name: str = Field("", description="Optional name of the threat to search for")

class NLPToolInput(BaseModel):
    content: str = Field(..., description="The text content to process for entity extraction")

class NLPTool(Tool):
    name: str = "NLP Tool"
    description: str = "Processes text to extract threat intelligence entities using Diffbot NLP."

    def __init__(self, diffbot_nlp):
        self.diffbot_nlp = diffbot_nlp
        super().__init__(
            name=self.name,
            description=self.description,
            func=self._run,
            args_schema=NLPToolInput
        )


    def _run(self, content: str) -> str:
        # Process the data to extract entities
        entities = self._extract_entities(content)
        return json.dumps(entities)
        
    def _extract_entities(self, content: str) -> Dict:
        # Use Diffbot NLP to extract entities
        nlp_result = self.diffbot_nlp.transform(content)
        
        # Initialize a dictionary to store extracted entities
        extracted_entities = {}
        
        # Extract entities based on EmergingThreat schema
        extracted_entities['name'] = self._extract_name(nlp_result)
        extracted_entities['description'] = self._extract_description(nlp_result)
        extracted_entities['threat_type'] = self._extract_threat_type(nlp_result)
        extracted_entities['severity'] = self._extract_severity(nlp_result)
        extracted_entities['status'] = self._extract_status(nlp_result)
        extracted_entities['confidence'] = self._extract_confidence(nlp_result)
        extracted_entities['tactics'] = self._extract_tactics(nlp_result)
        extracted_entities['techniques'] = self._extract_techniques(nlp_result)
        extracted_entities['threat_actors'] = self._extract_threat_actors(nlp_result)
        extracted_entities['malware_families'] = self._extract_malware_families(nlp_result)
        extracted_entities['indicators'] = self._extract_indicators(nlp_result)
        extracted_entities['targeted_sectors'] = self._extract_targeted_sectors(nlp_result)
        extracted_entities['targeted_countries'] = self._extract_targeted_countries(nlp_result)
        extracted_entities['references'] = self._extract_references(nlp_result)
        extracted_entities['last_updated'] = self._extract_last_updated(nlp_result)
        
        return extracted_entities

    # Helper methods to extract specific entities
    def _extract_name(self, nlp_result) -> str:
        # Logic to extract name from NLP result
        pass

    def _extract_description(self, nlp_result) -> str:
        # Logic to extract description from NLP result
        pass

    def _extract_threat_type(self, nlp_result) -> str:
        # Logic to extract threat type from NLP result
        pass

    def _extract_severity(self, nlp_result) -> str:
        # Logic to extract severity from NLP result
        pass

    def _extract_status(self, nlp_result) -> str:
        # Logic to extract status from NLP result
        pass

    def _extract_confidence(self, nlp_result) -> float:
        # Logic to extract confidence from NLP result
        pass

    def _extract_tactics(self, nlp_result) -> List[str]:
        # Logic to extract tactics from NLP result
        pass

    def _extract_techniques(self, nlp_result) -> List[str]:
        # Logic to extract techniques from NLP result
        pass

    def _extract_threat_actors(self, nlp_result) -> List[str]:
        # Logic to extract threat actors from NLP result
        pass

    def _extract_malware_families(self, nlp_result) -> List[str]:
        # Logic to extract malware families from NLP result
        pass

    def _extract_indicators(self, nlp_result) -> Dict[str, List[str]]:
        # Logic to extract indicators from NLP result
        return {
            "ip_addresses": [],
            "domains": [],
            "urls": [],
            "file_hashes": []
        }

    def _extract_targeted_sectors(self, nlp_result) -> List[str]:
        # Logic to extract targeted sectors from NLP result
        pass

    def _extract_targeted_countries(self, nlp_result) -> List[str]:
        # Logic to extract targeted countries from NLP result
        pass

    def _extract_references(self, nlp_result) -> List[str]:
        # Logic to extract references from NLP result
        pass

    def _extract_last_updated(self, nlp_result) -> str:
        # Logic to extract last updated date from NLP result
        pass


    def _extract_entities_from_text(self, text: str) -> Dict:
        # Implement text-based entity extraction here
        # This is where you'd use NLP techniques to extract entities from unstructured text
        # For now, we'll just return a placeholder
        return {"extracted_text": text}

class GraphUpdateInput(BaseModel):
    entities: str = Field(..., description="JSON string containing entities to update in the graph")

class GraphUpdateTool(BaseTool):
    name: str = "Graph Update Tool"
    description: str = "Creates or updates nodes and edges in the Neo4j graph database. Input should be a JSON string containing 'entities'."

    def __init__(self):
        super().__init__(
            func=self.run,
            args_schema=GraphUpdateInput
        )

    def run(self, entities: str) -> str:
        try:
            # Parse the input JSON string
            entities_data = json.loads(entities)
            graph_id = self._update_graph(entities_data)
            return json.dumps({"status": "success", "message":"Graph updated successfully. Graph ID: " + graph_id})
        except json.JSONDecodeError:
            return json.dumps({"status": "error", "message": "Invalid JSON input"})
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})
        
    def _update_graph(self, data: Dict) -> str:
        graph_id = str(uuid.uuid4())
        
        with GraphDatabase.driver(uri=self.neo4j_uri, auth=(self.neo4j_user, self.neo4j_password)) as driver:
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
