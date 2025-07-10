from fastapi import APIRouter, Body, Depends

from config import user_service
from service.conversation_service import ConversationService
from utils.get_current_user import JWTBearer

conversation_router = APIRouter()
conversation_service = ConversationService()


@conversation_router.post("/chat", dependencies=[Depends(JWTBearer(user_service))])
async def chat(query: str = Body(default="Your query...")):
    """
    POST endpoint that accepts a query as input and returns a response from the model.

    Args:
        query (str): The user's query to the model. Defaults to "Your query...".

    Returns:
        String: The model's response to the user's query.
    """
    return await conversation_service.chat(query)


@conversation_router.post("/new-chat", dependencies=[Depends(JWTBearer(user_service))])
async def new_chat(query: str = Body(default="Your query...")):
    """
    Invalidate the context (currently uploaded documents and chunks) and start a new conversation.

    Args:
        query (str): The user's query to the model. Defaults to "Your query...".

    Returns:
        String: The model's response to the user's query.
    """
    return await conversation_service.new_chat(query)
