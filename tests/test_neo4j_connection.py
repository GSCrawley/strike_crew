from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get environment variables
neo4j_uri = os.getenv('NEO4J_URI')
neo4j_user = os.getenv('NEO4J_USER')
neo4j_password = os.getenv('NEO4J_PASSWORD')

# # Debugging statements to verify environment variables
# print(f"Loaded from .env - NEO4J_URI: {neo4j_uri}")
# print(f"Loaded from .env - NEO4J_USER: {neo4j_user}")
# print(f"Loaded from .env - NEO4J_PASSWORD: {neo4j_password}")

# # Fallback to default if .env loading fails
# if not neo4j_password:
#     print("Falling back to default password")
#     neo4j_password = 'neo4jdbms'

# print(f"Using NEO4J_PASSWORD: {neo4j_password}")

def test_connection(uri, user, password):
    driver = GraphDatabase.driver(uri, auth=(user, password))
    try:
        driver.verify_connectivity()
        print("Connection successful")
    except Exception as e:
        print(f"Connection failed: {e}")
    finally:
        driver.close()

if __name__ == "__main__":
    test_connection(neo4j_uri, neo4j_user, neo4j_password)
