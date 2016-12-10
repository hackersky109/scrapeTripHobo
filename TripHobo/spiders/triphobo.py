import scrapy
from TripHobo.items import PathItem

#output json format : scrapy crawl triphobo -o triphobo.json

pagecnt = 0

class TripSpider(scrapy.Spider):
    name = 'triphobo'
    start_urls = ['https://www.triphobo.com/tripplans/chicago']

    def parse(self, response):
        for block in response.css('.js-block-list-item'):
            # follow links to subpages
            href = block.css('a::attr(href)').extract()[0]
            total_days = block.css('.blocklist-total-days::text').extract_first()
            views = block.css('.blocklist-total-views::text').extract_first()
            yield scrapy.Request(href,meta = {'views':views, 'total_days':total_days},callback=self.parse_plan)

        # follow pagination links
        global pagecnt
        next_page = response.css('li.next a::attr(href)').extract_first()
        if (next_page is not None) and (pagecnt<1) :
            pagecnt=pagecnt+1
            yield scrapy.Request(next_page,callback=self.parse)

    def parse_plan(self,response):
        item = PathItem()
        plan_list=[]
        item['title'] = response.xpath('//*[contains(@class, "step-2-itin-name")]/h1//text()|//*[contains(@class, "step-2-itin-name")]/h2//text()')[0].extract()
        item['total_days'] = response.meta['total_days']
        item['views'] = response.meta['views']
        item['startTime'] = response.xpath('//*[contains(@itemprop, "startTime")]//text()').extract()
        item['endTime'] = response.xpath('//*[contains(@itemprop, "endTime")]//text()').extract()

        startcity = response.xpath('//*[contains(@class, "start-city-name")]/span//text()').extract()
        if len(startcity) :
                item['start_city'] = startcity
        else:
                item['start_city']= response.xpath('//*[contains(@class, "transit-city")]/span//text()').extract()
        item['transit_city'] = response.xpath('//*[contains(@class, "transit-city")]/span//text()').extract()
        day_len = len(response.css('.js_day.active-day'))
        for day in response.css('.js_day.active-day'):
                if(len(day.css('h4.step-2-attraction-name::text').extract())):
                    plan_list.append(day.css('h4.step-2-attraction-name::text').extract())
        item['plan'] =plan_list
        yield item
