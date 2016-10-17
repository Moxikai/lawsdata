# -*- coding: utf-8 -*-
import json
import time
import scrapy

from scrapy import FormRequest,Request

class CaseSpider(scrapy.Spider):
    name = "case"
    post_url = 'http://lawsdata.com/home/search/searchJson'

    def start_requests(self):

        formdata={'type':'1',
                  'page':'1',
                  'searchTime':str(int(time.time())),
                  'searchNum':'20',
                  'nowReason':'0',
                  'keyword':'诈骗',
                  'TypeKey':'1:诈骗',
                  'judgement_id':'1',
                  }
        yield FormRequest(url=self.post_url,
                          formdata=formdata,
                          meta={'dont_cache':True},
                          dont_filter=True,
                          callback=self.parse,
                          )

    def parse(self, response):
        data = json.loads(response.body)

        total = data['info']['count'] # 当前搜索结果总数
        search_list = data['info']['searchList']['list'] # 当前页列表项
        page = data['info']['searchList']['page'] # 当前页码
        count = data['info']['searchList']['count'] # 当前页面列表项个数
        for item in search_list:
            url = 'http://lawsdata.com/detail/%s/'%(item['id'])
            yield Request(url=url,
                          meta={'item':item},
                          callback=self.parse_detail)

        if int(count) < 20:

            print '-----------------------当前页数据项小于20，已到最后一页，请检查----------------------------'
        else:
            print '准备转到页面----------%s------------'%(int(page)+1)
            formdata = {
                'type':'1',
                'page':str(int(page)+1),
                'searchTime':str(int(time.time())),
                'nowReason':'0',
                'keyword':'诈骗',
                'TypeKey':'1:诈骗',
                'judgement_id':'1',
            }
            yield FormRequest(url=self.post_url,
                              formdata=formdata,
                              dont_filter=True,
                              callback=self.parse)

    def parse_detail(self,response):
        """解析详情页面"""
        content = response.xpath('//div[@id="caseText"]').extract()
        item = response.meta['item']
        item['content'] = content
        yield item


