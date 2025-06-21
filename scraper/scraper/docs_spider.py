import scrapy
from pathlib import Path
from urllib.parse import urlparse

class DocsSpider(scrapy.Spider):
    name = "docs"

    def __init__(self, homepage_url, save_dir, *args, **kwargs):
        super(DocsSpider, self).__init__(*args, **kwargs)
        self.start_urls = [homepage_url]
        self.allowed_domains = [urlparse(homepage_url).netloc]
        self.save_dir = Path(save_dir)
        self.save_dir.mkdir(parents=True, exist_ok=True)

    def parse(self, response):
        # Save the content of the page
        filename = response.url.split("/")[-1] or "index.html"
        if not filename.endswith(('.html', '.htm')):
            filename += ".html"

        filepath = self.save_dir / filename
        with open(filepath, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')

        # Only follow links if this is an HTML response
        content_type = response.headers.get('Content-Type', b'').decode('utf-8', errors='ignore').lower()
        if 'text/html' in content_type:
            # Follow links to other pages on the same domain
            for href in response.css('a::attr(href)').getall():
                yield response.follow(href, self.parse)
        else:
            self.log(f'Skipping link extraction for non-HTML content: {content_type}')
