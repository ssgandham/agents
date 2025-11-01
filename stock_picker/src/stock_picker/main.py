#!/usr/bin/env python
import sys
import warnings
import os
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
project_root = Path(__file__).parent.parent.parent
env_path = project_root / '.env'
load_dotenv(dotenv_path=env_path)

# ChromaDB requires CHROMA_OPENAI_API_KEY - set it from OPENAI_API_KEY if not present
if not os.getenv('CHROMA_OPENAI_API_KEY') and os.getenv('OPENAI_API_KEY'):
    os.environ['CHROMA_OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

# Verify required API keys are loaded
if not os.getenv('OPENAI_API_KEY'):
    print("\n⚠️  ERROR: OPENAI_API_KEY not found!")
    print(f"Looking for .env file at: {env_path}")
    print("Please create a .env file with your OPENAI_API_KEY")
    print("\nExample .env file:")
    print("OPENAI_API_KEY=sk-your-key-here")
    print("SERPER_API_KEY=your-serper-key-here\n")
    sys.exit(1)

from stock_picker.crew import StockPicker

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    """
    Run the research crew.
    """
    inputs = {
        'sector': 'Technology',
        "current_date": str(datetime.now())
    }

    # Create and run the crew
    result = StockPicker().crew().kickoff(inputs=inputs)

    # Print the result
    print("\n\n=== FINAL DECISION ===\n\n")
    print(result.raw)


if __name__ == "__main__":
    run()