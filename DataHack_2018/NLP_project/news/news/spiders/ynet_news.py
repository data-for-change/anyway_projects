import scrapy
import re


class YNetNews(scrapy.Spider):
    name = "ynet_news"
    counter = 1

    def start_requests(self):
        urls = [
            'https://www.ynet.co.il/tags/%D7%AA%D7%90%D7%95%D7%A0%D7%95%D7%AA_%D7%93%D7%A8%D7%9B%D7%99%D7%9D',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for break_new in response.css('div.HeadlineListContainer div'):
            data = {
                'header': break_new.css('div.HeadlineTtl a.smallheader::text').extract_first(),
                'description': break_new.css('div.HeadlineSubTtl a.text12::text').extract_first(),
                'date_entity': break_new.css('div.HeadlineDetails::text').extract_first(),
            }

            if None not in data.values():
                data.update({'date': re.search('\d{2}\.\d{2}\.\d{2}', data['date_entity']).group(0)})
                data.update({'time': re.search('\d{2}\:\d{2}', data['date_entity']).group(0)})
                yield data

        next_page = 'https://www.ynet.co.il' + response.css('div.HeadlineListContainer div a::attr(href)')[-1].extract()
        # yield response.css('div.HeadlineListContainer div a.smallheader.HeadlinePrev::attr(href)').extract_first()
        self.counter -= 1
        if next_page is not None and self.counter:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
