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


class TripSpider(scrapy.Spider):
    name = 'triphobo'

    start_urls = ['https://www.triphobo.com/tripplans/chicago']

    def parse(self, response):
        # follow links to author pages
        for href in response.css('.blocklist-trip-name-wrapper a::attr(href)').extract():
            yield scrapy.Request(href,
                                 callback=self.parse_plan)

        # follow pagination links
        # next_page = response.css('li.next a::attr(href)').extract_first()
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)

    def parse_plan(self, response):
        def extract_with_css(query):
            return response.css(query).extract_first().strip()
        # #'start-city': extract_with_css('.start-city-name span::text')
        # yield {
        #     'transit-city': extract_with_css('.transit-city span::text'),
        # }
        tmp = response.xpath('//*[contains(@class, "transit-city")]/span//text()').extract()
        print tmp
        yield {
            'start-city': extract_with_css('.start-city-name span::text'),
            'transit-city': tmp,
        }
