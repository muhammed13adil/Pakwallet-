"""Configuration settings for PakWallet."""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    """Application settings."""

    app_name: str = os.getenv("APP_NAME", "PakWallet")
    tagline: str = os.getenv("TAGLINE", "Your Smart Financial Companion")
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///pakwallet.db")
    demo_user_email: str = os.getenv("DEMO_USER_EMAIL", "demo@pakwallet.pk")
    demo_user_password: str = os.getenv("DEMO_USER_PASSWORD", "PakWallet@123")


settings = Settings()
