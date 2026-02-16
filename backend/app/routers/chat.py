import json
import logging
from typing import AsyncGenerator

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from claude_agent_sdk import (
    ClaudeSDKClient,
    ClaudeAgentOptions,
    AssistantMessage,
    ResultMessage,
    TextBlock,
)
from app.agent.system_prompt import get_system_prompt
from app.agent.tools import info_tools_server
from app.middleware.rate_limit import rate_limit_dependency

logger = logging.getLogger(__name__)

router = APIRouter()


class ChatRequest(BaseModel):
    message: str
    session_id: str


async def _stream_agent(message: str) -> AsyncGenerator[bytes, None]:
    """Stream SSE events from the Claude Agent SDK.

    Uses explicit connect()/disconnect() lifecycle (not async-with)
    following the pattern from ai-oncall-bots. This avoids event-loop
    conflicts when running inside uvicorn.
    """
    options = ClaudeAgentOptions(
        system_prompt=get_system_prompt(),
        max_turns=3,
        mcp_servers={"info": info_tools_server},
        allowed_tools=[
            "mcp__info__get_github_repos",
            "mcp__info__get_project_details",
            "mcp__info__get_resume",
        ],
        permission_mode="bypassPermissions",
    )

    client = ClaudeSDKClient(options=options)

    try:
        await client.connect()
        await client.query(message)

        async for msg in client.receive_response():
            if isinstance(msg, AssistantMessage):
                for block in msg.content:
                    if isinstance(block, TextBlock):
                        data = json.dumps({"type": "text", "content": block.text})
                        yield f"data: {data}\n\n".encode()
            elif isinstance(msg, ResultMessage):
                if msg.is_error:
                    data = json.dumps(
                        {"type": "error", "content": msg.result or "Unknown error"}
                    )
                    yield f"data: {data}\n\n".encode()
                break

    except Exception as e:
        logger.exception("Error in agent")
        data = json.dumps({"type": "error", "content": str(e)})
        yield f"data: {data}\n\n".encode()

    finally:
        try:
            await client.disconnect()
        except Exception:
            pass

    done = json.dumps({"type": "done"})
    yield f"data: {done}\n\n".encode()


@router.post("/api/chat")
async def chat(
    request: ChatRequest,
    _rate_limit: None = Depends(rate_limit_dependency),
):
    """Stream a chat response as Server-Sent Events."""
    return StreamingResponse(
        _stream_agent(request.message),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
