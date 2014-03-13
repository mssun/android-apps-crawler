#!/bin/sh
scrapy crawl android_apps_spider -s JOBDIR=job -a market=$1
