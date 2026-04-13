import sys
from pathlib import Path

# Add src to path so we can import modules
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from api import app

# Vercel needs the app exported as 'app'
# The FastAPI app from backend/src/api.py is already named 'app'