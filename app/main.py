from fastapi import FastAPI, HTTPException, Response
from app.services.conversation import store

app = FastAPI(title="Argus")

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