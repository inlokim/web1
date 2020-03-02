import scrapy
from urllib.parse import urljoin
import re
from web1.items import Web1Item
from langdetect import detect
from bs4 import BeautifulSoup

class Web1Spider(scrapy.Spider):
    
    name = "web1"
    start_urls = [
        'https://www.ffwp.org/list/blank.php?menuKey=14',
        'https://www.ffwp.org/list/blank.php?menuKey=12',
        'https://www.ffwp.org/list/blank.php?menuKey=13',
        'https://www.ffwp.org/list/blank.php?menuKey=86',
        'https://www.ffwp.org/list/blank.php?menuKey=17'
    ]
    
    menuKey = '14'
    page = '4'

    def parse(self, response):

        #Category
        category = ""
        cate_arr = response.css('div.location li::text').getall()
        for cate in cate_arr:
            category += cate + ">"
        print('category : ', category)   


        news = response.css('div.grid div.grid-item')

        for n in news:

            img = urljoin(response.url, n.css('img::attr(src)').get())

            date = n.css('div.pro-grid-date::text').get()

            #Title
            title = n.css('div.pro-grid-title::text').get()
            
            # print("title : ", self.title)
            
            #Url
            main_url = urljoin(response.url, n.css('div.grid-item a::attr(href)').get())
            
            # print("url : ", self.url)

            num = n.css('div.grid-item a::attr(data-value)').get()
            
            # print("num : ", num)
            
            
            #content를 가져오기 위해
            
            content_url = "/list/viewCardFrame.php?num="+str(num)
            url = urljoin(response.url, content_url)
            
            request = scrapy.Request(url, 
                                    callback=self.parse_news, 
                                    cb_kwargs=dict(main_url=main_url))
                                    
            request.cb_kwargs['title'] = title                       
            request.cb_kwargs['category'] = category                       
            request.cb_kwargs['date'] = date  
            request.cb_kwargs['img'] = img  
            
            yield request

        # next_page_url = 'https://www.ffwp.org/include/function_ajax.php'
        # data = {'ajaxType' : 'thumbPageList',
        #         'sMenu':'14',
        #         'sPage':'4',
        #         'sMaxRows':'10',
        #         'searchTxt':'',
        #         'subMenu': '',
        #         'category': ''}
        
        # try:            
            
        #     yield scrapy.http.FormRequest(next_page_url, 
        #                             formdata=data, 
        #                             callback=self.parse)
            
        # except Exception as e:
        #     self.logger.warning(str(e))
        #     pass
                
            
    def parse_news(self, response, main_url, title, category, date, img):

        text = response.css('div.pro_viewPart').get()
        soup = BeautifulSoup(text)
        content = soup.get_text()
        
        # yield {
        #     'url' : main_url,
        #     'title' : title,
        #     'content': re.sub(r'(?u)[^-\w. ]', '', content)
        # }
        
        item = Web1Item()
        
        item_title = lang_dectect(title, "title")
        item_content = lang_dectect(content, "content")
        item[item_title] = title
        item[item_content] = re.sub(r'(?u)[^-\w. ]', '', content)
        item['url'] = main_url
        item['category'] = category
        item['date'] = date
        item['img'] = img
        
        yield item

def lang_dectect(text, postfix):
    
    try:
        lang = detect(text)

        if lang == "ko":
            result = "korean_" + postfix
        elif lang == "ja":
            result = "japanese_" + postfix
        elif lang == "zh-cn":
            result = "chinese_" + postfix
        elif lang == "en":
            result = "english_" + postfix
        else:
            result = postfix    
    except Exception as ex:
        print("lang : ",ex)
        result = postfix  
        
    return result
    
    
