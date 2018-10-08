from scrapy import cmdline
cmdline.execute("scrapy crawl ynet_news -o ynet_news.json".split())