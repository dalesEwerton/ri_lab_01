# -*- coding: utf-8 -*-
import scrapy
import json

from ri_lab_01.items import RiLab01Item
from ri_lab_01.items import RiLab01CommentItem


class DiarioDoCentroDoMundoSpider(scrapy.Spider):
    name = 'diario_do_centro_do_mundo'
    allowed_domains = ['diariodocentrodomundo.com.br']
    start_urls = []

    def __init__(self, *a, **kw):
        super(DiarioDoCentroDoMundoSpider, self).__init__(*a, **kw)
        with open('seeds/diario_do_centro_do_mundo.json') as json_file:
                data = json.load(json_file)
        self.start_urls = list(data.values())

    def parse(self, response):
        i = RiLab01Item()
        i['text'] = response.css('h3.td-module-title a::attr(href)').getall()
        i['author'] = response.url
        
        yield i
        
