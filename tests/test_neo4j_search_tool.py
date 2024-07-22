
import unittest
from strike_crew.tools.custom_tool import Neo4JSearchTool
from dotenv import dotenv
import os

from dotenv import load_dotenv
load_dotenv()


uri = os.getenv('NEO4J_URI')
user = os.getenv('NEO4J_USER')
password = os.getenv('NEO4J_PASSWORD')

class TestNeo4JSearchTool(unittest.TestCase):
    def test_initialization(self):
        try:
            tool = Neo4JSearchTool(uri=uri, user=user, password=password)
            print("Neo4JSearchTool initialized successfully.")
        except Exception as e:
            self.fail(f"Failed to initialize Neo4JSearchTool. Error: {e}")

    def test_query(self):
        tool = Neo4JSearchTool(uri="bolt://localhost:7687", user="neo4j", password="password")
        query = "MATCH (n) RETURN n LIMIT 1"
        result = tool.run(query)
        print(result)
        self.assertIn("Query failed", result) == False

if __name__ == '__main__':
    unittest.main()

