"""Anthropic client wrapper for the chatbot agent."""

import logging
from collections import OrderedDict
from typing import AsyncGenerator

import anthropic

from app.config import MODEL_NAME, get_anthropic_api_key
from app.agent.system_prompt import get_system_prompt
from app.agent.tools import TOOLS, execute_tool

logger = logging.getLogger(__name__)

MAX_SESSIONS = 50
MAX_HISTORY_MESSAGES = 40  # per session

# Ordered dict so we can evict the oldest session when the limit is reached.
_sessions: OrderedDict[str, list[dict]] = OrderedDict()


def _get_client() -> anthropic.AsyncAnthropic:
    """Create and return an async Anthropic client."""
    return anthropic.AsyncAnthropic(api_key=get_anthropic_api_key())


def _get_session_history(session_id: str) -> list[dict]:
    """Return the conversation history for a session, creating it if needed."""
    if session_id in _sessions:
        # Move to end (most recently used)
        _sessions.move_to_end(session_id)
        return _sessions[session_id]

    # Evict oldest session if at capacity
    if len(_sessions) >= MAX_SESSIONS:
        _sessions.popitem(last=False)

    _sessions[session_id] = []
    return _sessions[session_id]


def _trim_history(history: list[dict]) -> None:
    """Trim conversation history to stay within limits.

    Removes the oldest user/assistant pair(s) from the front while keeping
    the total number of messages at or below MAX_HISTORY_MESSAGES.
    """
    while len(history) > MAX_HISTORY_MESSAGES:
        # Remove messages from the front, always removing in pairs to keep
        # the alternating user/assistant pattern intact.
        history.pop(0)
        if history:
            history.pop(0)


async def get_chat_response(
    message: str, session_id: str
) -> AsyncGenerator[str, None]:
    """Stream a chat response for the given message.

    Yields text chunks as they are produced. Handles tool-use loops
    automatically: if the model requests a tool call, the tool is executed
    and the result is fed back so the model can continue generating text.
    """
    client = _get_client()
    system_prompt = get_system_prompt()
    history = _get_session_history(session_id)

    # Append the new user message
    history.append({"role": "user", "content": message})
    _trim_history(history)

    # We may loop if the model makes tool calls
    while True:
        try:
            async with client.messages.stream(
                model=MODEL_NAME,
                max_tokens=1024,
                system=system_prompt,
                messages=list(history),  # send a copy
                tools=TOOLS,
            ) as stream:
                # Collect the full response so we can store it in history
                collected_content: list[dict] = []
                current_text = ""
                tool_use_blocks: list[dict] = []

                async for event in stream:
                    if event.type == "content_block_start":
                        if event.content_block.type == "text":
                            current_text = ""
                        elif event.content_block.type == "tool_use":
                            tool_use_blocks.append(
                                {
                                    "type": "tool_use",
                                    "id": event.content_block.id,
                                    "name": event.content_block.name,
                                    "input": {},
                                }
                            )
                    elif event.type == "content_block_delta":
                        if event.delta.type == "text_delta":
                            current_text += event.delta.text
                            yield event.delta.text
                        elif event.delta.type == "input_json_delta":
                            # Accumulate tool input JSON incrementally.
                            # The SDK streams partial JSON; we append it as
                            # a string and parse at block_stop.
                            if tool_use_blocks:
                                block = tool_use_blocks[-1]
                                block.setdefault("_raw_input", "")
                                block["_raw_input"] += event.delta.partial_json
                    elif event.type == "content_block_stop":
                        if current_text:
                            collected_content.append(
                                {"type": "text", "text": current_text}
                            )
                            current_text = ""

                # Finalise tool_use blocks: parse accumulated JSON input
                import json as _json

                for block in tool_use_blocks:
                    raw = block.pop("_raw_input", "{}")
                    try:
                        block["input"] = _json.loads(raw) if raw else {}
                    except _json.JSONDecodeError:
                        block["input"] = {}
                    collected_content.append(block)

                # Get the final message to check stop_reason
                final_message = await stream.get_final_message()
                stop_reason = final_message.stop_reason

                # Store assistant response in history
                history.append({"role": "assistant", "content": collected_content})
                _trim_history(history)

            # If the model used tools, execute them and continue the loop
            if stop_reason == "tool_use" and tool_use_blocks:
                tool_results: list[dict] = []
                for block in tool_use_blocks:
                    tool_name = block["name"]
                    tool_input = block["input"]
                    logger.info(
                        "Executing tool %s with input %s", tool_name, tool_input
                    )
                    result = execute_tool(tool_name, tool_input)
                    tool_results.append(
                        {
                            "type": "tool_result",
                            "tool_use_id": block["id"],
                            "content": result,
                        }
                    )

                # Add tool results as a user message and loop
                history.append({"role": "user", "content": tool_results})
                _trim_history(history)
                continue  # go around the while-loop to get the model's follow-up

            # No more tool calls -- we're done
            break

        except anthropic.APIError as e:
            logger.exception("Anthropic API error")
            yield f"\n\n[Error communicating with AI service: {e.message}]"
            break
        except Exception as e:
            logger.exception("Unexpected error in chat response")
            yield f"\n\n[Unexpected error: {str(e)}]"
            break
