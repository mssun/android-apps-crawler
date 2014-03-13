#!/bin/sh
if [ $# -ne 2 ]
then
    echo "Usage: $0 <market name>"
    exit 2
fi

scrapy crawl android_apps_spider -s JOBDIR=job -a market=$1
