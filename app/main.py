import uuid

from fastapi import FastAPI, HTTPException, Response, Request
from app.services.conversation import store
from app.schemas.chat import ChatResponse, ChatRequest

from contextlib import asynccontextmanager
from app.clients.deepseek import DeepSeekClient


@asynccontextmanager  # 异步上下文管理器
async def lifespan(app: FastAPI):  # 定义应用生命周期
    """manage application-level resources"""
    # 共享客户端
    app.state.deepseek_client = DeepSeekClient()

    try:
        yield
    finally:
        await app.state.deepseek_client.close()

app = FastAPI(
    title="Argus",
    lifespan=lifespan,
)

@app.get("/health")
async def health_check():
    return {"status": "ok"}



@app.post("/conversations", status_code=201)
async def conversations():
    conversation = store.create()

    return {
        "conversation_id": conversation.conversation_id,
        "status": "active",
        "created_at": conversation.created_at.isoformat(),
    }

@app.delete("/conversations/{conversation_id}", status_code=204)
async def delete_conversation(conversation_id: str):
    conversation = store.get(conversation_id)

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail={
                "error":{
                    "code": "CONVERSATION_NOT_FOUND",
                    "message": "Conversation not found or expired",
                    "retryable": False
                }
            }
        )

    if not store.delete(conversation.conversation_id):
        raise HTTPException(
            status_code = 409,
            detail = {
                "error":{
                    "code": "CONVERSATION_BUSY",
                    "message": "cannot delete conversation while a task is active",
                    "retryable": False
                }
            }
        )

    return Response(status_code=204)


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, http_request: Request):
    conversation = store.get(str(request.conversation_id))

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "CONVERSATION_NOT_FOUND",
                "message": "Conversation not found or expired",
            }
        )

    #try to acquire the conversation lock without blocking
    if not conversation.lock.acquire(blocking=False):
        raise HTTPException(
            status_code=409,
            detail={
                "code": "CONVERSATION_BUSY",
                "message": "a task is already running in this conversation",
            }
        )

    try:
        conversation.touch()

        deepseek_client = http_request.app.state.deepseek_client

        messages = [
            {
                "role": "system",
                "content": "You are a helpful personal assistant.",
            },
            *conversation.messages,
            {
                "role": "user",
                "content": request.message,
            },
        ]

        answer = await deepseek_client.chat(messages)

        conversation.messages.append(
            {
                "role": "user",
                "content": request.message,
            }
        )

        conversation.messages.append(
            {
                "role": "assistant",
                "content": answer,
            }
        )
        return ChatResponse(
            task_id=uuid.uuid4(),
            conversation_id=request.conversation_id,
            status="completed",
            answer = answer,
            error=None
        )
    finally:
        conversation.lock.release()