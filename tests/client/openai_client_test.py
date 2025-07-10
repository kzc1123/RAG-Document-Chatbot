import unittest
from unittest.mock import MagicMock, patch

from client.openai_client import OpenAIClient
from config import API_KEY


class TestOpenAIClient(unittest.TestCase):

    def test_get_prompt(self):
        client = OpenAIClient(api_key=API_KEY)
        prompt = client.get_prompt(query="Test query")
        expected_prompt = {
            "role": "user",
            "content": "Test query"  # No refinement applied in this test case
        }
        self.assertEqual(prompt, expected_prompt)

    def test_get_prompt_for_context(self):
        client = OpenAIClient(api_key=API_KEY)
        prompt = client.get_prompt_for_context(context="Test context")
        expected_prompt = {
            "role": "user",
            "content": "Test context"
        }
        self.assertEqual(prompt, expected_prompt)

    def test_get_refined_query(self):
        client = OpenAIClient(api_key=API_KEY)
        refined_query = client.get_refined_query(query="Test query")
        # As there's no refinement logic implemented, the query should remain the same
        self.assertEqual(refined_query, "Test query")


if __name__ == "__main__":
    unittest.main()
