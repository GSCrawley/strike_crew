import os
from dotenv import load_dotenv
import pytest
from strike_crew.tools.custom_tool import Neo4JSearchTool

load_dotenv()

@pytest.fixture
def neo4j_tool():
    return Neo4JSearchTool(
        uri=os.environ.get("NEO4J_URI"),
        user=os.environ.get("NEO4J_USER"),
        password=os.environ.get("NEO4J_PASSWORD"),
        encrypted=os.environ.get("NEO4J_ENCRYPTED") == "True"
    )

def test_neo4j_search_tool(neo4j_tool):
    # Mock query for testing
    query = "Threat"
    result = neo4j_tool._run(query)
    assert isinstance(result, list)

