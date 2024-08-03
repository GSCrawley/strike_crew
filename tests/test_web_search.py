from crewai_tools import WebsiteSearchTool

def test_web_search():
    search_tool = WebsiteSearchTool()
    query = "latest Cybersecurity threats"
    results = search_tool._run(query)
    print("Web Search Results:", results)

if __name__ == "__main__":
    test_web_search()
a