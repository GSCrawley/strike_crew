from crewai_tools import BaseTool
from neo4j import GraphDatabase, exceptions
# from pydantic import PrivateAttr
from dotenv import load_dotenv
import os
import requests
import pprint
from bs4 import BeautifulSoup
from typing import Any, Dict, List, Optional
from langchain_community.graphs import Neo4jGraph
from langchain_experimental.graph_transformers.diffbot import DiffbotGraphTransformer
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_core.tools import Tool
from strike_crew.models import EmergingThreat, dataclasses


load_dotenv()

host = "bolt://localhost:7474"
uri = os.getenv('NEO4J_URI')
user = os.getenv('NEO4J_USER')
password = os.getenv('NEO4J_PASSWORD')
nlp = os.getenv('DIFFBOT_NLP_API_TOKEN')
custom_search = os.getenv('GOOGLE_API_KEY')
google_serper = os.getenv('GOOGLE_SERPER_API_KEY')
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
        print(schema)

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
    
class Neo4JSearchTool(BaseTool):
    name: str = "Neo4J Search"
    description: str = "A tool to query Neo4j database using APOC procedures."
    def __init__(self, uri, user, password):
        super().__init__()
        self._neo4j_db = Neo4jDatabase(host=uri, user=user, password=password)
        # Raise an error if the APOC plugin is not available
        try:
            self._neo4j_db.query("CALL apoc.help('apoc')")
        except Exception as e:
            raise ValueError("Missing APOC Core plugin") from e

    def _run(self, query: str) -> str:
        try:
            result = self._neo4j_db.query(query)
            return str(result)
        except Exception as e:
            return f"Query failed: {e}"

    def __del__(self):
        if hasattr(self, '_neo4j_db'):
            self._neo4j_db.close()


search = GoogleSerperAPIWrapper()
search_tool = Tool(
   
    name = "google_search",
    description = "Searches the web for information based on user queries.",
    func=search.run
)

class WebSearchTool(BaseTool):
    name: str = "Web Search"
    description: str = "Searches the web for information based on user queries."

    def _run(self, query: str, emerging_threat: EmergingThreat) -> list:
        # Fine-tune the search query with the indicators in the EmergingThreat dataclass
        refined_query = f"{query} {' '.join(emerging_threat.ioc.keys())} {' '.join(emerging_threat.ttps.keys())} {' '.join(emerging_threat.threat_actors)} {' '.join(emerging_threat.cve_ids)}"
        # Placeholder implementation - replace with actual web search logic or API call
        search_results = [
            "https://www.example.com/page1",
            "https://www.example.com/page2",
            "https://www.example.com/page3"
        ]
        return search_results
        # Placeholder implementation - replace with actual web search logic or API call
        search_results = [
            "https://www.example.com/page1",
            "https://www.example.com/page2",
            "https://www.example.com/page3"
        ]
        return search_results

class WebScraperTool(BaseTool):
    name: str = "Web Scraper"
    description: str = "Scrapes content from a list of URLs."

    def _run(self, urls: list) -> dict:
        results = {}
        for url in urls:
            try:
                response = requests.get(url)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
                text_content = soup.get_text()
                results[url] = text_content.strip()
            except requests.RequestException as e:
                results[url] = f"An error occurred while fetching the URL: {str(e)}"
        return results

class DiffbotNLPTool(BaseTool):
    name: str = "NLP Tool"
    description: str = "Processes text to extract threat intelligence entities."

    def _run(self, content: str) -> dict:
        # Use Diffbot NLP tool to process and sort scraped information into entities and relationships
        response = diffbot_nlp.nlp_request(content)
        entities = diffbot_nlp.process_response(response, content)
        return entities
        # Placeholder implementation - replace with actual NLP processing logic
        entities = {
            "threat_actors": ["Actor1", "Actor2"],
            "CVEs": ["CVE-2021-12345", "CVE-2021-67890"],
            "TTPs": ["Phishing", "Malware"],
            "IOCs": ["192.168.1.1", "example.com"]
        }
        return entities

class DiffbotGraphUpdateTool(BaseTool):
    name: str = "Neo4J Update"
    description: str = "Updates Neo4J database with new knowledge graphs."

    def __init__(self, uri, user, password):
        super().__init__()
        self._neo4j_db = Neo4jDatabase(host=uri, user=user, password=password)

    def _run(self, entities: dict) -> str:
        # Create new knowledge graphs in Neo4J using DiffbotGraphTransformer
        graph_documents = diffbot_nlp.convert_to_graph_documents(entities)
        graph.add_graph_documents(graph_documents)
        return "Neo4J database updated successfully."
        try:
            with self._neo4j_db._driver.session(database=self._neo4j_db._database) as session:
                for entity_type, entity_list in entities.items():
                    for entity in entity_list:
                        query = f"MERGE (e:{entity_type} {{name: '{entity}'}})"
                        session.run(query)
            return "Neo4J database updated successfully."
        except Exception as e:
            return f"Failed to update Neo4J database: {str(e)}"

    def close(self):
        self._neo4j_db._driver.close()
