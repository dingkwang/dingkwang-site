"""Claude Agent SDK client for the chatbot.

Uses ClaudeSDKClient as an async context manager per request,
following the pattern from the SDK examples.
"""

import logging
from typing import AsyncGenerator

from claude_agent_sdk import (
    ClaudeSDKClient,
    ClaudeAgentOptions,
    AssistantMessage,
    ResultMessage,
    TextBlock,
)

from app.agent.system_prompt import get_system_prompt
from app.agent.tools import info_tools_server

logger = logging.getLogger(__name__)


def _build_options() -> ClaudeAgentOptions:
    """Build ClaudeAgentOptions with MCP tools and system prompt."""
    def _stderr_callback(line: str) -> None:
        logger.info("SDK stderr: %s", line.rstrip())

    return ClaudeAgentOptions(
        system_prompt=get_system_prompt(),
        max_turns=3,
        mcp_servers={"info": info_tools_server},
        allowed_tools=[
            "mcp__info__get_github_repos",
            "mcp__info__get_project_details",
            "mcp__info__get_resume",
        ],
        permission_mode="bypassPermissions",
        stderr=_stderr_callback,
    )


async def get_chat_response(
    message: str, session_id: str
) -> AsyncGenerator[str, None]:
    """Stream a chat response for the given user message.

    Each call creates a fresh ClaudeSDKClient context manager which
    spawns a subprocess, handles tool calls via the MCP server, streams
    text back, and cleans up automatically.
    """
    options = _build_options()

    try:
        async with ClaudeSDKClient(options=options) as client:
            await client.query(message)

            async for msg in client.receive_response():
                if isinstance(msg, AssistantMessage):
                    for block in msg.content:
                        if isinstance(block, TextBlock):
                            yield block.text
                elif isinstance(msg, ResultMessage):
                    if msg.is_error:
                        logger.error("Agent error: %s", msg.result)
                        yield "\n\n[An error occurred while generating the response.]"
                    break

    except Exception as e:
        logger.exception("Error in chat response")
        yield f"\n\n[Error: {str(e)}]"
