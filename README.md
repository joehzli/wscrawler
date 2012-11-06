wscrawler
=========

WSCrawler is a crawler for a social website "weibo", which is China's twitter.

This crawler is written with python and is designed to be distributed.

There are two major components in this cralwer, one is the manager including a parser - wscrawler.py & parsewb.py, and another one is the downloader - downloader/wsdownloader.py
The manager can use multiple downloaders. The downloader's address is configured in variable wscrawler.downloaders.

This crawler is still under development.
