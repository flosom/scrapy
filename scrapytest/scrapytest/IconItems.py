#引入文件
import scrapy

class IconItems(scrapy.Item):
    name = scrapy.Field()
    firsturl=scrapy.Field()
    secondurl = scrapy.Field()
    website = scrapy.Field()
    whitepaper = scrapy.Field()
    #社交网站
    soclinks=scrapy.Field()
    #公募时间
    time = scrapy.Field()
    #Token标识
    ticker=scrapy.Field()
    price = scrapy.Field()
    #硬顶
    hardgoal=scrapy.Field()
    #总发行量
    totaltokens=scrapy.Field()
    availablesale=scrapy.Field()
    bonusrate=scrapy.Field()
    accepts=scrapy.Field()

   
    
