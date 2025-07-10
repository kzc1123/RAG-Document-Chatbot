from client.openai_client import OpenAIClient
from config import API_KEY, faiss, initialize_faiss
from utils.logger import logger


class ConversationService:
    def __init__(self):
        self.vdb = faiss
        self.open_ai_client = OpenAIClient(API_KEY)
        self.default_message = {
            "role": "system",
            "content": "You are a RAG application which receives a set of texts similar to user prompt, "
                       "and you answer the question using those set of texts. You may provide inputs from your side "
                       "as well. "
        }

        self.context = ""
        self.max_history = 2
        self.prompt_list = []

    async def chat(self, query: str):

        prompt = self.open_ai_client.get_prompt(query)
        self.prompt_list.append(prompt)
        if len(self.prompt_list) > self.max_history:
            self.prompt_list.pop(0)

        similar_docs = self.vdb.similarity_search(query)

        if len(similar_docs) > 0:
            context = similar_docs[0].page_content
        else:
            context = ""

        context_prompt = self.open_ai_client.get_prompt_for_context(context)

        messages = [self.default_message, context_prompt]
        messages = messages + self.prompt_list
        logger.info(messages)
        llm_response = await self.open_ai_client.get_chat_response(messages)
        return llm_response

    async def new_chat(self, query: str):
        self.prompt_list = []
        self.context = ""
        # initialize_faiss() not to be done, Just for a new chat there will be no message context.
        # self.vdb = faiss

        prompt = self.open_ai_client.get_prompt(query)
        self.prompt_list.append(prompt)

        messages = [self.default_message]
        messages = messages + self.prompt_list
        logger.info(messages)
        llm_response = await self.open_ai_client.get_chat_response(messages)
        return llm_response
