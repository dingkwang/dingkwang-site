import os
from dotenv import load_dotenv

load_dotenv()


def get_anthropic_api_key() -> str:
    """Return the Anthropic API key. Raises if not set."""
    key = os.getenv("ANTHROPIC_API_KEY")
    if not key:
        raise RuntimeError(
            "ANTHROPIC_API_KEY environment variable is required. "
            "Set it in a .env file or export it in your shell."
        )
    return key


ALLOWED_ORIGINS: list[str] = [
    origin.strip()
    for origin in os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
    if origin.strip()
]

RATE_LIMIT_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "10"))

MODEL_NAME: str = os.getenv("MODEL_NAME", "claude-sonnet-4-20250514")
