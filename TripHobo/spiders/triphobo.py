import scrapy
from TripHobo.items import PathItem
#output json format : scrapy crawl triphobo -o triphobo.json

count = 0

class TripSpider(scrapy.Spider):
    name = 'triphobo'
    start_urls = ['https://www.triphobo.com/tripplans/chicago']

    def parse(self, response):

        for block in response.css('.itinerary-blocklist-wrapper'):
            # follow links to subpages
            href = block.css('a::attr(href)').extract()[0]
            views = block.css('.blocklist-total-views::text').extract_first()
            yield scrapy.Request(href,meta = {'views':views},callback=self.parse_plan)

        # follow pagination links
        global count
        next_page = response.css('li.next a::attr(href)').extract_first()
        if (next_page is not None) and (count<1) :
            count=count+1
            yield scrapy.Request(next_page,callback=self.parse)

    def parse_plan(self,response):
        item = PathItem()

        item['title'] = response.xpath('//*[contains(@class, "step-2-itin-name")]/h1//text()|//*[contains(@class, "step-2-itin-name")]/h2//text()')[0].extract()
        item['views'] = response.meta['views']
        startcity = response.xpath('//*[contains(@class, "start-city-name")]/span//text()').extract()
        if len(startcity) :
                item['start_city'] = startcity
        else:
                item['start_city']= response.xpath('//*[contains(@class, "transit-city")]/span//text()').extract()
        item['transit_city'] = response.xpath('//*[contains(@class, "transit-city")]/span//text()').extract()

        yield item
