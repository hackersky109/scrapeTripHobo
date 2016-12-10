import scrapy
import re
import json
import requests
from scrapy.http import FormRequest
from TripHobo.items import PathItem
from scrapy.selector import Selector
from scrapy.selector import XmlXPathSelector
from scrapy.selector import HtmlXPathSelector
import lxml.etree as etree
import dicttoxml
#output json format : scrapy crawl triphobo -o triphobo.json

pagecnt = 0

class TripSpider(scrapy.Spider):
    name = 'test'
    start_urls = ['https://www.triphobo.com/tripplans/chicago']

    def parse(self, response):
        pat = '[a-zA-Z0-9]+'
        for block in response.css('.js-block-list-item'):

            # follow links to subpages
            href = block.css('a::attr(href)').extract()[0]
            nodeID = block.css('li::attr(id)').extract()[0]
            getId = re.findall(pat,nodeID)[-1]
            loadAll_href ="https://www.triphobo.com/itinerary/loadDayOnView/" + getId
            total_days = block.css('.blocklist-total-days::text').extract_first()
            views = block.css('.blocklist-total-views::text').extract_first()
            yield scrapy.Request(href,meta = {'views':views, 'total_days':total_days,'loadAll_href':loadAll_href,'id':getId},callback=self.parse_plan)

        # follow pagination links
        global pagecnt
        next_page = response.css('li.next a::attr(href)').extract_first()
        if (next_page is not None) and (pagecnt<1) :
            pagecnt=pagecnt+1
            yield scrapy.Request(next_page,callback=self.parse)

    def parse_plan(self,response):
        item = PathItem()
        qq=[]
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

        loadAll_href = response.meta['loadAll_href']
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        form_data = {"start":'5',"limit":'20'}
        # r = requests.post(loadAll_href,data=form_data,headers=headers)
        print("RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRr")
        # print(r.text)
        print("RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR")
        cnt=0
        cntt=0
        day_len = len(response.css('.js_day.active-day'))
        for day in response.css('.js_day.active-day'):
                print("SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS")
                # cnt=cnt+1
                # if cnt > 5:
                #     r = requests.post(loadAll_href,data=form_data,headers=headers)
                #     print(r.text)
                if(len(day.css('h4.step-2-attraction-name::text').extract())):
                    cnt = cnt + 1
                    qq.append(day.css('h4.step-2-attraction-name::text').extract())
                    qq.append('@')
                else:
                    if(cntt==0):
                        cntt=cntt+1
                        yield FormRequest(loadAll_href,method='POST',formdata = form_data,callback=self.ppparse_plan)

        item['plan'] =qq
        yield item

    def ppparse_plan(self,response):
         print("BBBBBBBBBBBBBBBBBBBBBBBBQ")
        #  jsonresponse = json.loads(response.body_as_unicode())
        #  json_dict = jsonresponse["itinerary_day_html"]
         sel = HtmlXPathSelector(response)
         data = sel.xpath('//*[contains(@class, "step-2-attraction-name")]//text()').strip('\r\n\t').extract()
         print(data)
         print("QQQQQQQQQQQQQQQQQQQQQQQQB")
