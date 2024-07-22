from crewai_tools import ScrapeWebsiteTool

def test_web_scraper():
    scraper_tool = ScrapeWebsiteTool()
    urls = ["https://www.example.com/page1", "https://www.example.com/page2"]
    results = scraper_tool._run(urls)
    print("Web Scraper Results:", results)

if __name__ == "__main__":
    test_web_scraper()
