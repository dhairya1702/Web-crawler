# Web Crawler

An asynchronous web crawler built with Python, Playwright, and BeautifulSoup. This project efficiently scrapes websites for specific links while adhering to politeness rules and user-defined filtering criteria.

---

## 🚀 Features

- **Asynchronous Crawling**: Uses Playwright for high-performance, non-blocking web scraping.
- **Intelligent Filtering**: Crawls and filters links based on domain and path patterns.
- **Politeness**: Includes delays between requests to avoid overloading servers.
- **Customizable Settings**: Modify starting URLs, maximum crawl depth, and output file.

---

## 📸 Demo

![Crawler Demo](demo_screenshot.png)  
*(Replace this with a screenshot or GIF of your crawler running.)*

---

## 📂 Project Structure

```plaintext
web-crawler/
├── src/
│   ├── crawler.py              # The main crawler script
├── tests/
│   ├── test_crawler.py         # Unit tests for your crawler
├── data/
│   ├── visited_links.txt       # Output file with crawled links
├── requirements.txt            # Dependencies
├── README.md                   # Documentation
├── .gitignore                  # Files to ignore in version control
├── LICENSE                     # Project license 

```

## 🛠️ Installation

Follow these steps to set up and run the project locally:

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/web-crawler.git
cd web-crawler
```

### Step 2: Install Dependencies
Install the required Python packages using the following command:
```bash
pip install -r requirements.txt
```

### Step 3: Install Playwright
Set up Playwright for browser automation by running:
```bash
playwright install
```

### Step 4: Run the Crawler
Execute the crawler script to start crawling:
```bash
python src/crawler.py
```


## ⚙️ Configuration

You can customize the following settings in `src/crawler.py` to tailor the crawler to your needs:

- **Initial URLs**: Update the `urls_to_crawl` list in the `main()` function to specify the starting URLs for the crawl.
- **Maximum URLs**: Set the `max_urls` parameter in the `Crawler` class to define the maximum number of URLs to visit during a crawl.
- **Output File**: Modify the `output_file` parameter to specify the file where the visited URLs will be saved (default: `visited_links.txt`).


