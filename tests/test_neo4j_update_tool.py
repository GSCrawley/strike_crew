from strike_crew.tools.custom_tool import Neo4JUpdateTool
from dotenv import load_dotenv
import os


load_dotenv()

uri = os.getenv('NEO4J_URI')
user = os.getenv('NEO4J_USER')
password = os.getenv('NEO4J_PASSWORD')


def test_neo4j_update_tool():
    update_tool = Neo4JUpdateTool(uri=uri, user=user, password=password)
    entities = {
        "threat_actors": ["Actor1", "Actor2"],
        "CVEs": ["CVE-2021-12345", "CVE-2021-67890"],
        "TTPs": ["Phishing", "Malware"],
        "IOCs": ["192.168.1.1", "example.com"]
    }
    result = update_tool._run(entities)
    print("Neo4J Update Tool Result:", result)
    update_tool.close()

if __name__ == "__main__":
    test_neo4j_update_tool()
