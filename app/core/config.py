"""
Application configuration module.

This module is responsible for:
- Loading environment variables
- Managing environment-specific behavior (development vs production)
- Centralizing all configuration values
- Validating required settings at startup
"""

import os
from dotenv import load_dotenv


# Determine current environment (default: development)
ENV = os.getenv("ENV", "development")


# Load environment variables from `.env` file
# Only used for local development and testing
if ENV != "production":
    load_dotenv()


class Config:
    """
    Central configuration class.

    All application-wide settings should be accessed
    through this class to ensure consistency.
    """
    # Database connection URLs
    DATABASE_URL = os.getenv("DATABASE_URL")
    
# Validate required environment variables in production
# Fail fast to prevent misconfigured deployments
if ENV == "production":
    required = [
        "DATABASE_URL"
    ]

    missing = [var for var in required if not os.getenv(var)]
    if missing:
        raise RuntimeError(f"Missing required env vars: {missing}")

if Config.DATABASE_URL and Config.DATABASE_URL.startswith("postgresql://"):
    Config.DATABASE_URL = Config.DATABASE_URL.replace(
        "postgresql://",
        "postgresql+psycopg2://",
        1,
    )
