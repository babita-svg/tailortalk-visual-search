"""TailorTalk Main Application Entry Point.

Runs the Streamlit visual retrieval and conversational stylist interface.
"""

from pathlib import Path
import sys

# Add project root to Python module path
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Import and execute the UI
from ui.streamlit_app import main

if __name__ == "__main__":
    main()
