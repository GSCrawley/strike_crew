from strike_crew.tools.custom_tool import NLPTool

def test_nlp_tool():
    nlp_tool = NLPTool()
    content = "Sample text containing threat intelligence."
    results = nlp_tool._run(content)
    print("NLP Tool Results:", results)

if __name__ == "__main__":
    test_nlp_tool()
