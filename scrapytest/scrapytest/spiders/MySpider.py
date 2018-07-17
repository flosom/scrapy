#引入文件
import scrapy
from scrapy.http import Request
from scrapytest.IconItems import IconItems

class MySpider(scrapy.spiders.Spider):
    #用于区别Spider
    name = "MySpider"
    #允许访问的域
    allowed_domains = ["icodrops.com"]
    #爬取的地址
    start_urls = ["https://icodrops.com/category/ended-ico/",
        "https://icodrops.com/category/upcoming-ico/",
       "https://icodrops.com/category/active-ico/"]
   #第一级url爬取方法
    def parse(self, response):
        items=[]
        #这部分是爬取部分，使用xpath的方式选择信息，具体方法根据网页结构而定
        for box in response.xpath('//div[@class="tabs__content active"]//div[@class="ico-icon"]'):
             #实例一个容器保存爬取的信息
            item = IconItems()
            item['status'] = response.url
            second_url = box.xpath('.//a/@href').extract()[0]
            item['secondurl'] = second_url
            items.append(item)
            #拼接第二层url
            if second_url:
                yield Request(url=item['secondurl'], meta={'item_1': item},callback=self.parse1)
                
    #第二级url爬取方法
    def parse1(self, response):
        items = response.meta['item_1']
        for box in response.xpath('//div[@class="row justify-content-center"]'):
            item = IconItems()
            item['status']=items['status'].split('/')[-2]
            item['name'] =box.xpath('.//div[@class="ico-main-info"]//h3/text()').extract()[0]
            #item['secondurl']=items['secondurl']
            item['website']=box.xpath('.//div[@class="ico-right-col"]/a/@href').extract()[0]
            item['whitepaper']=box.xpath('.//div[@class="ico-right-col"]/a/@href').extract()[1]
            
            #以下是获取social links
            socials=[]
            socialwebs=box.xpath('.//div[@class="ico-right-col"]/div[@class="soc_links"]//a/@href').extract()
            i=0
            for i in range(len(socialwebs)):
                url = socialwebs[i]
                socials.append(url)
            item['soclinks']=socials
            #以下是获取公募时间
            time=box.xpath('.//div[@class="col-12 title-h4"][1]/h4/text()').extract()
            print("".join(time).replace(' ','').replace("\n", "").split()[1])
            item['time']="".join(time).replace(' ','').replace("\n", "").split()[1]
            #以下是获取二级url右侧数据
            dataright=box.xpath('.//div[@class="col-12 col-md-6"][2]/li//span/text()').extract()
            k=0
            right_item=[];
            for element1 in dataright:
                right_item.append(element1)
                if element1=='Accepts: ':
                    item['accepts']=box.xpath('.//div[@class="col-12 col-md-6"][2]/li/text()').extract()[-1]
               # elif element=='ICO Token Price:':
               #     item['price']=box.xpath('.//div[@class="col-12 col-md-6"][2]/li/text()').extract()[k]
                k=k+1
            #补齐空字段
            #二级url空字段处理
            icon_items_right=['Accepts: ']
            #集合差集
            difflist=list(set(icon_items_right).difference(set(right_item)))
            for ele in difflist:
                if ele=='Accepts: ':
                    item['accepts']='无数据'
                    
            #以下是获取二级url左侧数据
            dataleft=box.xpath('.//div[@class="col-12 col-md-6"][1]/li//span/text()').extract()
            j=0
            left_item=[];
            
            for element in dataleft:
                left_item.append(element)
                if element=='Ticker: ':
                    item['ticker']=box.xpath('.//div[@class="col-12 col-md-6"][1]/li/text()').extract()[j]
                elif element=='ICO Token Price:':
                    item['price']=box.xpath('.//div[@class="col-12 col-md-6"][1]/li/text()').extract()[j]
                elif element=='Fundraising Goal:':
                    item['hardgoal']=box.xpath('.//div[@class="col-12 col-md-6"][1]/li/text()').extract()[j]
                elif element=='Total Tokens: ':
                    item['totaltokens']=box.xpath('.//div[@class="col-12 col-md-6"][1]/li/text()').extract()[j]
                elif element=='Available for Token Sale: ':
                    item['availablesale']=box.xpath('.//div[@class="col-12 col-md-6"][1]/li/text()').extract()[j]
                j=j+1
                
            #补齐空字段
            #二级url空字段处理
            icon_items=['Ticker: ','ICO Token Price:','Fundraising Goal:','Total Tokens: ','Available for Token Sale: ']
            #集合差集
            difflist=list(set(icon_items).difference(set(left_item)))
            for ele in difflist:
                if ele=='Ticker: ':
                    item['ticker']='无数据'
                elif ele=='ICO Token Price:':
                    item['price']='无数据'
                elif ele=='Fundraising Goal:':
                    item['hardgoal']='无数据'
                elif ele=='Total Tokens: ':
                    item['totaltokens']='无数据'
                elif ele=='Available for Token Sale: ':
                    item['availablesale']='无数据'
                
            #返回信息
            yield item
