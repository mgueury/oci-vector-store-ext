# Scrapy settings for scraper project
BOT_NAME = 'scraper'
SPIDER_MODULES = ['scraper.spiders']
NEWSPIDER_MODULE = 'scraper.spiders'

# Obey robots.txt rules - set to False for this example to ensure full crawling
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# This helps with avoiding being blocked
DOWNLOAD_DELAY = 1

# User-Agent string to use for all requests
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'

# Logging level
LOG_LEVEL = 'INFO'

# Configure the CSV feed export
FEED_FORMAT = 'csv'
FEED_URI = '/tmp/crawler/links.csv'
# Define the order of the fields in the CSV file
FEED_EXPORT_FIELDS = ['url', 'filename','title']