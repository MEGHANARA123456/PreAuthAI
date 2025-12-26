import os
from dotenv import load_dotenv

load_dotenv()

# ===== LLM COMMON CONFIG =====
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", 0.2))
LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", 800))

# ===== AWS BEDROCK (OPTIONAL) =====
AWS_REGION = os.getenv("AWS_REGION")
CLAUDE_MODEL_ID = os.getenv(
    "CLAUDE_MODEL_ID",
    "anthropic.claude-3-sonnet-20240229-v1:0"
)

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

# ===== GOOGLE GEMINI (OPTIONAL) =====
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GEMINI_MODEL_ID = os.getenv("GEMINI_MODEL_ID", "gemini-1.5-pro")
# --------------------------------------------------
# Email Settings (Password Reset)
# --------------------------------------------------
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT") or 587)
EMAIL_USERNAME = os.getenv("EMAIL_USERNAME")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_FROM = os.getenv("EMAIL_FROM",)

FRONTEND_RESET_URL = os.getenv(
    "FRONTEND_RESET_URL",
    "http://localhost:3000/reset-password"
)


'''import os
from dotenv import load_dotenv

load_dotenv()

# LLM selection
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "claude")  # claude | gemini

# Shared model config
LLM_MODEL_ID = os.getenv("LLM_MODEL_ID")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", 0.2))
LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", 800))

# Claude (AWS Bedrock)
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

# Google Gemini
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
#GOOGLE_PROJECT_ID = os.getenv("GOOGLE_PROJECT_ID")'''