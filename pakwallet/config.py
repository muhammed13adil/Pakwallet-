"""Configuration settings for PakWallet."""

import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """Application settings class."""
    
    @property
    def app_name(self) -> str:
        return os.getenv("APP_NAME", "PakWallet")

    @property
    def tagline(self) -> str:
        return os.getenv("TAGLINE", "Your Smart Financial Companion")

    @property
    def demo_user_email(self) -> str:
        return os.getenv("DEMO_USER_EMAIL", "demo@pakwallet.pk")

    @property
    def demo_user_password(self) -> str:
        return os.getenv("DEMO_USER_PASSWORD", "PakWallet@123")

settings = Settings()
