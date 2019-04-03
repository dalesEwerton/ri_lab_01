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
    sections = ['Brasil', 'Politica', 'Mundo', 'Comportamento', 'Economia', 'Esporte', 'Cultura', 'Destaques', 'analise', 'aovivo', 'Humor', 'Religião']

    def parse(self, response):
        links = []
        newLinks = []
        if response.url in self.start_urls:
            # NAV
            links = response.css('h3.td-module-title a::attr(href)').getall()
            for link in links:
                yield response.follow(link, callback=self.parse)
        else:
            # PARSE
            item = RiLab01Item()
            item['_id']       = self.id
            item['author']    = response.css('div.td-post-author-name a::text').get()
            item['date']      = response.css('span.td-post-date time::attr(datetime)').get()
            item['title']     = response.css('title::text').get()
            item['sub_title'] = 'N/A'
            item['section']   = self.getSection(response)
            item['text']      = self.getText(response)
            item['url']       = response.url
            self.id           = self.id + 1
            yield item
            if self.id < 200:
				# NAV
                link = response.css('div.td-post-next-prev-content a::attr(href)').get() 
                yield response.follow(link, callback=self.parse)
            
            
    def getText(self, response):
        textlist = response.css('p.p1 span.s1::text, p::text').getall()
        finalTextList = []
        for t in textlist:
            if 'O jornalismo do DCM precisa de você' not in t:
                finalTextList.append(t)
        return finalTextList
        
    def getSection(self, response):
        contentList = response.css('meta::attr(content)').getall()
        for content in contentList:
            if content in self.sections:
                return content
        return 'N/A'
