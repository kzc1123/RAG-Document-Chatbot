from openai import OpenAI


class OpenAIClient:
    """
    Client for OpenAI API.

    Provides methods for interacting with the OpenAI API for text generation.

    Args:
        api_key (str): The API key for accessing the OpenAI API.
    """

    def __init__(self, api_key):
        """
        Initializes the OpenAIClient.

        Initializes the OpenAI client with the provided API key and sets default temperature for text generation.

        Args:
            api_key (str): The API key for accessing the OpenAI API.
        """
        self.client = OpenAI(api_key=api_key)
        self.TEMPERATURE = 1.0

    async def get_chat_response(self, prompt_message):
        """
        Get response from the chat model.

        Generates a response from the chat model based on the provided prompt message.

        Args:
            prompt_message (str): The prompt message for generating the response.

        Returns:
            str: The generated response.

        Raises:
            Exception: If there's an error during response generation.
        """
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=prompt_message,
                # temperature=self.TEMPERATURE,
                # max_tokens=20,
            )
            return response.choices[0].message.content
        except Exception as e:
            raise e

    def get_prompt(self, query):
        """
        Get a prompt for processing query correctly for GPT API.

        Generates a prompt for processing the query correctly using GPT API.

        Args:
            query (str): The query string.

        Returns:
            dict: The prompt for the query.
        """
        return {
            "role": "user",
            "content": self.get_refined_query(query)
        }

    def get_prompt_for_context(self, context):
        """
        Get a prompt for processing context correctly.

        Generates a prompt for processing the context correctly using GPT API.

        Args:
            context (str): The context text.

        Returns:
            dict: The prompt for the context.
        """
        return {
            "role": "user",
            "content": context
        }

    def get_refined_query(self, query):
        """
        Refine the query for better search results.

        Refines the query for better search results.

        Args:
            query (str): The query string.

        Returns:
            str: The refined query.
        """
        # Currently returning the query as it is, should be refined for the app use case
        return query
