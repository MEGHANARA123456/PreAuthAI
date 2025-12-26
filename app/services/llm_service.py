from langchain_aws import ChatBedrock
from langchain_google_genai import ChatGoogleGenerativeAI

from app.config import (
    AWS_REGION,
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    CLAUDE_MODEL_ID,
    GOOGLE_API_KEY,
    GEMINI_MODEL_ID,
    LLM_TEMPERATURE,
    LLM_MAX_TOKENS
)

def get_llm():
    """
    Auto-select LLM based on available credentials.
    Priority:
    1. AWS Bedrock Claude
    2. Google Gemini
    """

    #  Use Claude ONLY if AWS credentials exist
    if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:
        return ChatBedrock(
            model_id=CLAUDE_MODEL_ID,
            region=AWS_REGION,
            temperature=LLM_TEMPERATURE,
            max_tokens=LLM_MAX_TOKENS
        )

    #  Fallback to Gemini (NO AWS REQUIRED)
    if GOOGLE_API_KEY:
        return ChatGoogleGenerativeAI(
            model=GEMINI_MODEL_ID,
            google_api_key=GOOGLE_API_KEY,
            temperature=LLM_TEMPERATURE,
            max_output_tokens=LLM_MAX_TOKENS
        )

    # No credentials
    raise RuntimeError(
        "No LLM credentials found. "
        "Set AWS credentials or GOOGLE_API_KEY in .env"
    )
