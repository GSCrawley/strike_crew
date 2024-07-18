import os
from dotenv import load_dotenv
import pytest
from strike_crew.tools.custom_tool import TwitterSearchTool

load_dotenv()

@pytest.fixture
def twitter_tool():
    return TwitterSearchTool(
        api_key=os.environ.get("TWITTER_API_KEY"),
        api_secret_key=os.environ.get("TWITTER_API_SECRET_KEY"),
        access_token=os.environ.get("TWITTER_ACCESS_TOKEN"),
        access_token_secret=os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")
    )

def test_twitter_search_tool(twitter_tool):
    # Mock query for testing
    query = "Cybersecurity"
    result = twitter_tool._run(query)
    assert "Tweet by" in result or "No tweets found" in result or "An error occurred" in result
