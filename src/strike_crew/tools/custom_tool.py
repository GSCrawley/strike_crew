from crewai_tools import BaseTool
import tweepy
from neo4j import GraphDatabase

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

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        super().__init__()

    def _run(self, text: str) -> bool:
        """
        Search the Neo4J database to validate if the text contains known cyberattack techniques.
        
        Args:
            text (str): The text to search within.
        
        Returns:
            bool: True if the text matches known techniques, False otherwise.
        """
        labels = ["AttackTechnique", "IndicatorOfCompromise"]  # Adjust the labels as necessary
        with self.driver.session() as session:
            for label in labels:
                result = session.run(
                    f"MATCH (n:{label}) WHERE $text CONTAINS n.name RETURN n",
                    text=text
                )
                if result.single() is not None:
                    return True
        return False

    def close(self):
        self.driver.close()

# Example usage within a task
if __name__ == "__main__":
     # Replace with your actual Twitter API credentials
    api_key = "your_api_key"
    api_secret_key = "your_api_secret_key"
    access_token = "your_access_token"
    access_token_secret = "your_access_token_secret"

    twitter_tool = TwitterSearchTool(api_key, api_secret_key, access_token, access_token_secret)
    query = "cybersecurity threats"
    result = twitter_tool._run(query)
    print(result)
    neo4j_tool = Neo4JSearchTool(uri='bolt://localhost:7687', user='neo4j', password='password')
    intelligence_list = ["phishing attempt detected", "malware spread via email"]  # Example data
    results = [neo4j_tool._run(intelligence) for intelligence in intelligence_list]

    for intelligence, is_valid in zip(intelligence_list, results):
        print(f"Intelligence: {intelligence}, Valid: {is_valid}")
    
    neo4j_tool.close()
    twitter_tool.close()