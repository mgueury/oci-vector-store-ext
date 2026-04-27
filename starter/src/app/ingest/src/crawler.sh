#!/bin/bash
cd crawler
echo "--- crawler.sh"
export PATH=$PATH:~/.local/bin
source ../../myenv/bin/activate
scrapy crawl crawler_spider -a url=$1