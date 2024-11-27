import pytest
import asyncio
from src.web_crawler import Crawler


@pytest.mark.asyncio
async def test_crawler_initialization():
    """
    Test if the Crawler class initializes with correct attributes.
    """
    initial_urls = ["https://example.com"]
    max_urls = 10
    output_file = "test_visited_links.txt"

    crawler = Crawler(urls=initial_urls, max_urls=max_urls, output_file=output_file)

    assert crawler.urls == initial_urls
    assert crawler.max_urls == max_urls
    assert crawler.output_file == output_file
    assert crawler.visited_urls == set()
    assert crawler.urls_to_visit == set(initial_urls)


@pytest.mark.asyncio
async def test_add_url_to_visit():
    """
    Test if the add_url_to_visit method correctly adds URLs to the queue.
    """
    initial_urls = ["https://example.com"]
    crawler = Crawler(urls=initial_urls)

    new_url = "https://example.com/page"
    crawler.add_url_to_visit(new_url)

    assert new_url in crawler.urls_to_visit
    assert new_url not in crawler.visited_urls


@pytest.mark.asyncio
async def test_link_extraction():
    """
    Test the get_linked_urls method to ensure it extracts and filters links correctly.
    """
    base_url = "https://example.com"
    sample_html = """
    <html>
        <body>
            <a href="/page1">Page 1</a>
            <a href="https://example.com/page2">Page 2</a>
            <a href="https://otherdomain.com/page">External Link</a>
        </body>
    </html>
    """
    crawler = Crawler(urls=[])
    extracted_links = list(crawler.get_linked_urls(base_url, sample_html))

    # Check that only internal links are returned
    assert len(extracted_links) == 2
    assert "https://example.com/page1" in extracted_links
    assert "https://example.com/page2" in extracted_links
    assert "https://otherdomain.com/page" not in extracted_links


@pytest.mark.asyncio
async def test_crawl_single_url():
    """
    Test the crawl method to ensure it processes a single URL.
    """
    initial_urls = ["https://example.com"]
    crawler = Crawler(urls=initial_urls, max_urls=1)

    # Mock the download_url method to return static HTML
    crawler.download_url = asyncio.coroutine(lambda _: """
    <html>
        <body>
            <a href="/page1">Page 1</a>
        </body>
    </html>
    """)

    await crawler.crawl(initial_urls[0])

    # Check that the crawler added the new URL
    assert "https://example.com/page1" in crawler.urls_to_visit
    assert initial_urls[0] in crawler.visited_urls
