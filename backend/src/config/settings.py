import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

class Settings:
    def __init__(self):
        # Load environment variables from .env file
        # Look for .env in the project root (parent of backend directory)
        project_root = Path(__file__).parent.parent.parent.parent
        env_path = project_root / ".env"
        if env_path.exists():
            load_dotenv(env_path)
        
        # Environment
        self.agent_env = os.getenv("AGENT_ENV", "development")
        
        # API Keys
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        
        # Security
        self.encryption_key = os.getenv("ENCRYPTION_KEY")
        
        # Logging
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        
        # Database
        # Use /tmp for serverless environments (Vercel, Lambda, etc.), otherwise use local data/
        if self.agent_env == "production":
            self.db_path = Path("/tmp/agent.db")
        else:
            self.db_path = Path("data/agent.db")
            try:
                self.db_path.parent.mkdir(exist_ok=True)
            except OSError:
                # If we can't write to data/ (e.g., read-only filesystem), use /tmp
                self.db_path = Path("/tmp/agent.db")

        # Logging
        # Use /tmp for serverless environments
        if self.agent_env == "production":
            self.log_file = Path("/tmp/agent.log")
        else:
            self.log_file = Path("logs/agent.log")
            try:
                self.log_file.parent.mkdir(exist_ok=True)
            except OSError:
                # If we can't write to logs/ (e.g., read-only filesystem), use /tmp
                self.log_file = Path("/tmp/agent.log")
        
        # Debug mode
        self.debug = self.agent_env == "development"
        
        # API Configuration
        self.api_host = "0.0.0.0"
        self.api_port = 8000
        
        # Frontend Configuration
        self.frontend_url = "http://localhost:3000"

# Global settings instance
settings = Settings()