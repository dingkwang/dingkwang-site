import json
import logging
from typing import AsyncGenerator

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse

from app.agent.client import get_chat_response
from app.middleware.rate_limit import rate_limit_dependency

logger = logging.getLogger(__name__)

router = APIRouter()


class ChatRequest(BaseModel):
    message: str
    session_id: str


async def _event_stream(message: str, session_id: str) -> AsyncGenerator[str, None]:
    """Generate SSE events from the agent's streaming response."""
    try:
        async for chunk in get_chat_response(message, session_id):
            event = {"type": "text", "content": chunk}
            yield json.dumps(event)
        yield json.dumps({"type": "done"})
    except Exception as e:
        logger.exception("Error during chat streaming")
        error_event = {"type": "error", "content": f"An error occurred: {str(e)}"}
        yield json.dumps(error_event)
        yield json.dumps({"type": "done"})


@router.post("/api/chat")
async def chat(
    request: ChatRequest,
    _rate_limit: None = Depends(rate_limit_dependency),
):
    """Stream a chat response as Server-Sent Events."""
    return EventSourceResponse(
        _event_stream(request.message, request.session_id),
        media_type="text/event-stream",
    )
