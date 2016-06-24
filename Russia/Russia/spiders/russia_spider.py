import scrapy
import re
import sys

from scrapy.selector import Selector
from Russia.items import RussiaItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.exceptions import CloseSpider

reload(sys)
sys.setdefaultencoding('utf-8')

class RussiaSpider(scrapy.Spider):

    name = "russia"

    allowed_domains = ['http://juku.yicool.cn/fn/ajax/ajax_SentenceInfo.ashx']
    
    ############## This need to be change ###################
    urls = open('./Url/Split/urlExpand_0_2.txt')
    start_urls = [ url.strip() for url in urls.readlines() ]
    urls.close()
    
    def parse(self, response):

        item = RussiaItem()
        
        # self.get_pageNum(response, item)
        
        self.get_sentence(response, item)
        yield item
    
    def get_pageNum(self, response, item):
        
        cleanr = re.compile('<.*?>')
        
        content = response.xpath('//*').extract()
        
        cleantext = re.sub( cleanr, '', content[0] )
        
        pageNum = open('./Url/pageNum.txt', 'a')

        with open('./init.html', 'w') as fout:
            fout.write(cleantext)
        
        with open('./init.html', 'r') as fin:
            for line in fin:
                numOfPages = line.split(',')[1].split(':')[1].strip('"')
                
                # print response.url
                print numOfPages
                
                pageNum.write( str(response.url) + ' ' + str(numOfPages) + '\n' )
                pageNum.close()

    def get_sentence(self, response, item):
        
        # ru_regex = r'^"ru":*+,$'
        # cn_regex = r''
        
        try:
            cleanr = re.compile('<.*?>')
            sentence = response.xpath("//*").extract()
            cleantext = re.sub(cleanr, '', sentence[0])
            
            if cleantext.startswith('{"totalsize'):
                ######### This needs to be change ############# 
                fout = open("./Sentence/sentence_0_2.txt", "a")
                fout.write( cleantext + '\n' )
                fout.close()
        except IndexError:
            print response.url
            # continue
            

