#!/bin/sh
if [ $# -le 0 ]
then
    echo "Usage: $0 <market name> [database output directory]"
    echo "   market name:"
    echo "       appchina.com"
    echo "       hiapk.com"
    echo "       anzhi.com"
    echo "       android.d.cn"
    echo "       mumayi.com "
    echo "       gfan.com"
    echo "       nduoa.com"
    echo "       3gyu.com"
    echo "       angeeks.com"
    echo "       appfun.cn"
    echo "       jimi168.com"
    echo "   database output directory:"
    echo "       default: ../repo/databases/"
    exit 2
fi

if [ $# -eq 1 ]
then
    scrapy crawl android_apps_spider -s JOBDIR=job_$1 -a market=$1
else
    scrapy crawl android_apps_spider -s JOBDIR=job_$1 -a market=$1 -a database_dir=$2
fi
