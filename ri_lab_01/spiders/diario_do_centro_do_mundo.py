# -*- coding: utf-8 -*-
import scrapy
import json

from ri_lab_01.items import RiLab01Item
from ri_lab_01.items import RiLab01CommentItem



class DiarioDoCentroDoMundoSpider(scrapy.Spider):
    name = 'diario_do_centro_do_mundo'
    allowed_domains = ['diariodocentrodomundo.com.br']
    start_urls = []
    id = 1

    def __init__(self, *a, **kw):
        super(DiarioDoCentroDoMundoSpider, self).__init__(*a, **kw)
        with open('seeds/diario_do_centro_do_mundo.json') as json_file:
            data = json.load(json_file)
        self.start_urls = list(data.values())

    def parse(self, response):
        links = []
        if response.url in self.start_urls:
            # NAV
            links = response.css('h3.td-module-title a::attr(href)').getall()
            for link in links:
                yield response.follow(link, callback=self.parse)
        else:
            # PARSE
            i = RiLab01Item()
            i['_id'] = self.id
            i['author'] = response.css('div.td-post-author-name a::text').get()
            i['date'] = response.css('span.td-post-date time::attr(datetime)').get()
            i['title'] = response.css('title::text').get()
            i['text'] = response.css('p.p1 span.s1::text').getall()
            i['url'] = response.url
            self.id = self.id + 1
            yield i
