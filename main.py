import uvicorn
from fastapi import FastAPI

from router.document import document_router
from router.conversation import conversation_router
from router.user import user_router

app = FastAPI()

app.include_router(document_router, prefix="", tags=["document_router"])
app.include_router(conversation_router, prefix="", tags=["conversation_router"])
app.include_router(user_router, prefix="", tags=["user_router"])


@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)