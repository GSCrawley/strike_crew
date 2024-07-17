from crewai_tools import BaseTool
import tweepy
from neo4j import GraphDatabase
from pydantic import PrivateAttr, Field
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Example tweet data for testing
Tweet = """This week started with an RCE in OpenSSH
CVE-2024-6387 affects OpenSSH versions from 8.5p1 to 9.7p1 and is a regression of an old flaw, 
CVE-2006-5051. An unauthenticated attacker can gain root access on glibc-based Linux systems, 
but they need to trigger a race condition and win the race. 
Researchers who discovered and responsibly disclosed the vulnerability say it typically takes ten thousand attempts — 
under default OpenSSH settings, the attack takes 6-8 hours. According to Censys and Shodan, 
around 14 million potentially vulnerable hosts are accessible on the Internet.
(https://qualys.com/2024/07/01/cve-2024-6387/regresshion.txt…)
To prevent the vulnerability, named regreSSHion, from haunting you like Log4shell, 
it is recommended to update OpenSSH and restrict access to devices running the OpenSSH service using network access control tools. 
Remember, this includes not only servers but also many IoT devices.
#news #vulnerabilities #linux #cybersecurity
"""

class TwitterSearchTool(BaseTool):
    name: str = "Search Twitter"
    description: str = (
        "Use this tool to search Twitter for the latest news about Cybersecurity threats."
    )
    api: tweepy.API = Field(default=None, exclude=True)  # Define the 'api' attribute

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, api_key, api_secret_key, access_token, access_token_secret):
        super().__init__()
        auth = tweepy.OAuth1UserHandler(api_key, api_secret_key, access_token, access_token_secret)
        self.api = tweepy.API(auth)

    def _run(self, query: str) -> str:
        try:
            tweets = self.api.search_tweets(q=query, count=1)
            if tweets:
                tweet = tweets[0]
                return f"Tweet by {tweet.user.screen_name}: {tweet.text}"
            else:
                return "No tweets found for the given query."
        except Exception as e:
            return f"An error occurred: {str(e)}"

class Neo4JSearchTool(BaseTool):
    name: str = "Neo4J Search Tool"
    description: str = "Searches the Neo4J database to validate if the text contains known cyberattack techniques."
    _driver: PrivateAttr() 

    class Config():
        arbitrary_types_allowed = True

    def __init__(self, uri, user, password, encrypted=False):
        super().__init__()
        self._driver = GraphDatabase.driver(uri, auth=(user, password), encrypted=encrypted)

    def _run(self, text: str) -> bool:
        """
        Search the Neo4J database to validate if the text contains known cyberattack techniques.
        
        Args:
            text (str): The text to search within.
        
        Returns:
            bool: True if the text matches known techniques, False otherwise.
        """
        labels = ["AttackTechnique", "IndicatorOfCompromise"]  # Adjust the labels as necessary
        with self._driver.session() as session:
            for label in labels:
                result = session.run(
                    f"MATCH (n:{label}) WHERE $text CONTAINS n.name RETURN n",
                    text=text
                )
                if result.single() is not None:
                    return True
        return False

    def close(self):
        self._driver.close()