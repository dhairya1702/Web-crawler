import asyncio
import logging
from urllib.parse import urljoin, urlparse
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

# Configure logging to display crawl progress and errors
logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO
)


class Crawler:
    """
    A web crawler class to asynchronously scrape websites for specific links.

    Attributes:
        urls (list): List of initial URLs to start crawling from.
        max_urls (int): Maximum number of URLs to crawl.
        output_file (str): File to save visited URLs.
        visited_urls (set): Set of already visited URLs.
        urls_to_visit (set): Set of URLs pending to be crawled.
    """

    def __init__(self, urls=[], max_urls=100, output_file='visited_links.txt'):
        """
        Initialize the crawler with starting URLs, max URLs to visit, and output file for results.
        """
        self.urls = urls
        self.max_urls = max_urls
        self.output_file = output_file
        self.visited_urls = set()
        self.urls_to_visit = set(urls)

    def save_visited_urls(self):
        """
        Save the visited URLs to the output file.
        Appends new URLs to avoid overwriting previous results.
        """
        with open(self.output_file, 'a') as file:
            for url in self.visited_urls:
                file.write(url + '\n')

    async def init_browser(self):
        """
        Initialize the Playwright browser instance.
        Configures the browser with a custom user agent and JavaScript support.
        """
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.firefox.launch(headless=True)
        self.context = await self.browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0',
            ignore_https_errors=True,
            java_script_enabled=True,
        )
        self.page = await self.context.new_page()

    async def close_browser(self):
        """
        Close the browser and clean up Playwright resources.
        """
        await self.browser.close()
        await self.playwright.stop()

    async def download_url(self, url):
        """
        Fetch the content of a URL using Playwright.

        Args:
            url (str): The URL to fetch.

        Returns:
            str or None: The HTML content of the page, or None if an error occurs.
        """
        try:
            await self.page.goto(url, wait_until='domcontentloaded', timeout=180000)
            await self.page.wait_for_load_state('networkidle', timeout=180000)
            return await self.page.content()
        except Exception as e:
            logging.error(f'Error downloading {url}: {e}')
            return None

    def get_linked_urls(self, base_url, html):
        """
        Extract and filter links from the provided HTML content.

        Args:
            base_url (str): The base URL for resolving relative links.
            html (str): The HTML content to parse for links.

        Yields:
            str: Filtered URLs that match specified criteria.
        """
        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.find_all('a', href=True):
            path = link['href']
            if path.startswith('/'):
                path = urljoin(base_url, path)  # Resolve relative paths
            elif not path.startswith('http'):
                continue
            # Check if the link belongs to the same domain as the base URL
            if urlparse(path).netloc == urlparse(base_url).netloc:
                # Filter URLs based on specific substrings
                # if "our-insights" in path or "featured-insights" in path or "new-at-mckinsey-blog" in path or '/publications' in path:
                #     if 'publications' in path:
                #         if '2023' in path or '2024' in path:
                #             yield path
                #     else:
                #         yield path
                yield path

    def add_url_to_visit(self, url):
        """
        Add a URL to the set of URLs to visit, ensuring it hasn't been visited yet.

        Args:
            url (str): The URL to add to the queue.
        """
        if url not in self.visited_urls and url not in self.urls_to_visit:
            self.urls_to_visit.add(url)

    async def crawl(self, url):
        """
        Crawl a single URL, download its content, and extract more links to visit.

        Args:
            url (str): The URL to crawl.
        """
        html = await self.download_url(url)
        if html:
            for new_url in self.get_linked_urls(url, html):
                self.add_url_to_visit(new_url)

    async def run(self):
        """
        Main method to start crawling. Iteratively processes URLs from the queue.
        """
        await self.init_browser()  # Initialize the browser
        try:
            while self.urls_to_visit and len(self.visited_urls) < self.max_urls:
                url = self.urls_to_visit.pop()
                logging.info(f'Crawling: {url}')
                try:
                    await self.crawl(url)
                except Exception as e:
                    logging.exception(f'Failed to crawl: {url}. Error: {e}')
                finally:
                    self.visited_urls.add(url)
                    self.save_visited_urls()
                await asyncio.sleep(5)  # Politeness delay between requests
        finally:
            await self.close_browser()  # Ensure browser is closed


async def main():
    """
    Entry point for the web crawler script. Define URLs to crawl and initiate the crawler.
    """
    urls_to_crawl = [
        "https://www.forbes.com/sites/digital-assets/2024/11/27/sudden-panic-sparks-200-billion-bitcoin-and-crypto-price-crash/"
    ]

    for url in urls_to_crawl:
        logging.info(f"Starting crawl for: {url}")
        crawler = Crawler(urls=[url], max_urls=50, output_file='visited_links.txt')
        await crawler.run()
        logging.info(f"Finished crawl for: {url}")
        logging.info(f"Visited {len(crawler.visited_urls)} pages for {url}")


if __name__ == '__main__':
    asyncio.run(main())
