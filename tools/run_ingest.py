# tools/run_ingest.py
import sys
from pathlib import Path

# Add project root to the path
sys.path.append(str(Path(__file__).parent.parent))

from src.doki.ingestion import ingest_from_html

# --- CONFIGURATION ---
HTML_SOURCE_DIR = Path(__file__).parent.parent / "data/scraped_html"

if __name__ == "__main__":
    ingest_from_html(HTML_SOURCE_DIR)
