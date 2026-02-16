import os
from dotenv import load_dotenv

load_dotenv()

ALLOWED_ORIGINS: list[str] = [
    origin.strip()
    for origin in os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
    if origin.strip()
]

RATE_LIMIT_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "10"))

MODEL_NAME: str = os.getenv("MODEL_NAME", "claude-sonnet-4-20250514")
