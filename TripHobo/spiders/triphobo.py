# import scrapy
#
#
# class TripSpider(scrapy.Spider):
#     name = "triphobo"
#     start_urls = [
#         'https://www.triphobo.com/tripplans/chicago',
#     ]
#
#     def parse(self, response):
#         for plan in response.css('div.itinerary-blocklist-wrapper'):
#             yield {
#                 'planname': plan.css('p::text')[0].extract(),
#             }

import scrapy
# scrapy crawl triphobo -o triphobo.json

count = 0
class TripSpider(scrapy.Spider):
    name = 'triphobo'
    start_urls = ['https://www.triphobo.com/tripplans/chicago']

    def parse(self, response):

        # follow links to author pages
        for href in response.css('.blocklist-trip-name-wrapper a::attr(href)').extract():
            yield scrapy.Request(href,callback=self.parse_plan)

        # follow pagination links
        global count
        next_page = response.css('li.next a::attr(href)').extract_first()
        if (next_page is not None) and (count<1) :
            count=count+1
            # next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_plan(self, response):
        yield {
            # 'title': extract_with_css('.step-2-itin-name h1::text'),
            'title': response.xpath('//*[contains(@class, "step-2-itin-name")]/h1//text()|//*[contains(@class, "step-2-itin-name")]/h2//text()')[0].extract(),
            'start-city': response.xpath('//*[contains(@class, "start-city-name")]/span//text()').extract(),
            'transit-city': response.xpath('//*[contains(@class, "transit-city")]/span//text()').extract(),
        }
