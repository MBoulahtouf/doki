# tools/run_scraper.py
import sys
from pathlib import Path
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

# Add scraper to the path
sys.path.append(str(Path(__file__).parent.parent / 'scraper'))

from scraper.docs_spider import DocsSpider

# --- CONFIGURATION ---
URL = "https://ramanspy.readthedocs.io/"
OUTPUT_DIR = "data/scraped_html"

if __name__ == '__main__':
    # Scrapy settings
    settings = Settings()
    settings.set("LOG_LEVEL", "INFO")
    settings.set("USER_AGENT", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36")
    settings.set("ROBOTSTXT_OBEY", True)
    settings.set("DEPTH_LIMIT", 5) # How deep to crawl

    process = CrawlerProcess(settings)
    process.crawl(DocsSpider, homepage_url=URL, save_dir=OUTPUT_DIR)
    process.start()
