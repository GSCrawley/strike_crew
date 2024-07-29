import unittest
from unittest.mock import patch, MagicMock

class TestDiffbotGraphUpdateTool(unittest.TestCase):
    @patch('strike_crew.tools.custom_tool.DiffbotGraphUpdateTool._driver')
    @patch('strike_crew.tools.custom_tool.DiffbotGraphUpdateTool._diffbot_nlp')
    @patch('strike_crew.tools.custom_tool.DiffbotGraphUpdateTool._graph')
    def test_run(self, mock_graph, mock_diffbot_nlp, mock_driver):
        # Mock session
        mock_session = MagicMock()
        mock_driver.session.return_value.__enter__.return_value = mock_session

        # Mock methods
        mock_diffbot_nlp.convert_to_graph_documents.return_value = "mock_graph_documents"
        mock_graph.add_graph_documents.return_value = None

        # Create tool instance
        tool = DiffbotGraphUpdateTool()

        # Define entities
        entities = {
            "Person": ["Alice", "Bob"],
            "Company": ["Acme Corp"]
        }

        # Run the tool
        result = tool._run(entities)

        # Print actual calls to mock_session.run
        print("Actual calls to mock_session.run:", mock_session.run.call_args_list)

        # Assertions
        self.assertEqual(result, "Neo4J database updated successfully.")
        mock_diffbot_nlp.convert_to_graph_documents.assert_called_once_with(entities)
        mock_graph.add_graph_documents.assert_called_once_with("mock_graph_documents")
        mock_session.run.assert_any_call("MERGE (e:Person {name: 'Alice'})")
        mock_session.run.assert_any_call("MERGE (e:Person {name: 'Bob'})")
        mock_session.run.assert_any_call("MERGE (e:Company {name: 'Acme Corp'})")

if __name__ == '__main__':
    unittest.main()