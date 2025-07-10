import unittest
from unittest.mock import MagicMock, patch

from service.conversation_service import ConversationService
import client
import utils

class TestConversationService(unittest.TestCase):
    def setUp(self):
        self.conversation_service = ConversationService()

    @patch('client.openai_client.OpenAIClient.get_prompt')
    @patch('client.openai_client.OpenAIClient.get_chat_response')
    @patch('utils.logger.logger.info')
    def test_chat_with_context(self, mock_logger_info, mock_get_chat_response, mock_get_prompt):
        query = "test query"
        context = "test context"
        mock_get_prompt.return_value = "test prompt"
        mock_get_chat_response.return_value = "test response"
        self.conversation_service.vdb.similarity_search = MagicMock(return_value=[MockDocument(page_content=context)])

        result = self.conversation_service.chat(query)

        mock_get_prompt.assert_called_once_with(query)
        self.assertEqual(self.conversation_service.prompt_list, ["test prompt"])
        self.conversation_service.vdb.similarity_search.assert_called_once_with(query)
        mock_logger_info.assert_called_once_with([self.conversation_service.default_message, "test prompt"])
        mock_get_chat_response.assert_called_once_with([self.conversation_service.default_message, "test prompt"])

        self.assertEqual(result, "test response")

    @patch('client.openai_client.OpenAIClient.get_prompt')
    @patch('client.openai_client.OpenAIClient.get_chat_response')
    @patch('utils.logger.logger.info')
    def test_chat_without_context(self, mock_logger_info, mock_get_chat_response, mock_get_prompt):
        query = "test query"
        mock_get_prompt.return_value = "test prompt"
        mock_get_chat_response.return_value = "test response"
        self.conversation_service.vdb.similarity_search = MagicMock(return_value=[])

        result = self.conversation_service.chat(query)

        mock_get_prompt.assert_called_once_with(query)
        self.assertEqual(self.conversation_service.prompt_list, ["test prompt"])
        self.conversation_service.vdb.similarity_search.assert_called_once_with(query)
        mock_logger_info.assert_called_once_with([self.conversation_service.default_message, "test prompt"])
        mock_get_chat_response.assert_called_once_with([self.conversation_service.default_message, "test prompt"])

        self.assertEqual(result, "test response")

    @patch('client.openai_client.OpenAIClient.get_prompt')
    @patch('client.openai_client.OpenAIClient.get_chat_response')
    @patch('utils.logger.logger.info')
    def test_new_chat(self, mock_logger_info, mock_get_chat_response, mock_get_prompt):
        query = "test query"
        mock_get_prompt.return_value = "test prompt"
        mock_get_chat_response.return_value = "test response"

        result = self.conversation_service.new_chat(query)

        mock_get_prompt.assert_called_once_with(query)
        self.assertEqual(self.conversation_service.prompt_list, ["test prompt"])
        mock_logger_info.assert_called_once_with([self.conversation_service.default_message, "test prompt"])
        mock_get_chat_response.assert_called_once_with([self.conversation_service.default_message, "test prompt"])

        self.assertEqual(result, "test response")


class MockDocument:
    def __init__(self, page_content):
        self.page_content = page_content


if __name__ == '__main__':
    unittest.main()
