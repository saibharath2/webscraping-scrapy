import scrapy,re
from scrapy.spidermiddlewares.httperror import HttpError 
from twisted.internet.error import DNSLookupError 
from twisted.internet.error import TimeoutError, TCPTimedOutError  
import csv
from datetime import datetime
import time

filename = 'magicbricks_project_{}_{}.csv'.format(datetime.now().year,datetime.now().month)
# with open(filename, 'w') as csvfile:
#     csvwriter = csv.writer(csvfile)
            
            
            
class MagicbricksCrawlSpider(scrapy.Spider):
    name = "magicbricks_crawl"
    allowed_domains = ["www.magicbricks.com"]
    start_urls = ["https://www.magicbricks.com/Real-estate-projects-Search/residential--new-project?proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment&cityName=New-Delhi"]
    HTTPERROR_ALLOWED_CODES = [301]
    
    def parse(self, response):
        headers = {
    'accept': 'text/response,application/xresponse+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-IN,en-US;q=0.9,en;q=0.8,te;q=0.7,hi;q=0.6',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (Kresponse, like Gecko) Chrome/126.0.0.0 Safari/537.36',
}

        cities_list = ['New-Delhi','Bangalore','Mumbai', 'Hyderabad', 'Thane', 'Pune', 'New', 'Chennai', 'Ahmedabad', 
               'Kolkata', 'Gurgaon', 'Noida', 'Navi-mumbai','ghaziabad', 'Jaipur', 'Lucknow', 'Coimbatore', 'Mysore',
               'Trivandrum', 'Visakhapatnam','nagpur','faridabad', 'Dehradun','chandigarh']
#         cities_list = ['New-Delhi']
        for ct in cities_list:
            city_url = 'https://www.magicbricks.com/Real-estate-projects-Search/residential--new-project?proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment&cityName={}'.format(ct)
        
            yield scrapy.Request(city_url,method='GET',headers=headers, callback=self.parse_city,meta={'city_name':ct,'pg_no':1},dont_filter=False,errback=self.errback_httpbin)
            
    def parse_city(self,response):
        headers = {
    'accept': 'text/response,application/xresponse+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-IN,en-US;q=0.9,en;q=0.8,te;q=0.7,hi;q=0.6',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (Kresponse, like Gecko) Chrome/126.0.0.0 Safari/537.36',
}
        city_name = response.meta['city_name']
        pg_no = response.meta['pg_no']
        try:
            city_code = response.meta['city_code']
        except:
            city_code = response.xpath('//@data-citycode').extract_first()
        all_pg_urls = response.xpath('//*[@id="projectSearchResultWrapper"]/div/@onclick').extract()
        if not all_pg_urls:
            all_pg_urls = response.xpath('//*[@class="srpBlockListRow"]/@onclick').extract()
        for url_txt in all_pg_urls:
            time.sleep(0.5)
            url = re.search(r"openProjectDetailPage\(event, '([^']+)", url_txt).group(1)
            yield scrapy.Request(url,method='GET',headers=headers, callback=self.parse_listing,meta={'city_name':city_name,'city_code':city_code,'pg_no':pg_no},dont_filter=False,errback=self.errback_httpbin)
        if len(all_pg_urls)!=0:
            print('more pages')
            pg_no = pg_no+1
            headers = {
                'accept': 'text/html, */*; q=0.01',
                'accept-language': 'en-IN,en-US;q=0.9,en;q=0.8,te;q=0.7,hi;q=0.6',
                'priority': 'u=1, i',
                'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"macOS"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
                'x-requested-with': 'XMLHttpRequest',
            }
            
            url2 = 'https://www.magicbricks.com/mbsearch/projectSearch.html?groupstart=1&p1=10002_10003_10021_10022_10020&postedSince=-1&city={}&searchType=5&p2=10002,10003,10021,10022,10020&p3=10002,10003,10021,10022&category=S&page={}'.format(city_code,pg_no)
    
            
            yield scrapy.Request(url2,method='GET',headers=headers, callback=self.parse_city,meta={'city_name':city_name,'city_code':city_code,'pg_no':pg_no},dont_filter=False,errback=self.errback_httpbin)
            
            
    def parse_listing(self,response):
        city_name = response.meta['city_name']
        city_code = response.meta['city_code']
        pg_no = response.meta['pg_no']
        project_url = response.url
        try:
            project_name = response.xpath('//span[@id="domcache_project"]/@data-psmname').extract_first()
        except:
            project_name = None
        try:
            project_developer = response.xpath('//span[@id="domcache_project"]/@data-devname').extract_first()
        except:
            project_developer = None
        try:
            locality = response.xpath('//span[@id="domcache_project"]/@data-locality').extract_first()
        except:
            locality = None
        try:
            city = response.xpath('//span[@id="domcache_project"]/@data-city').extract_first()
        except:
            city = None
        try:
            project_type = response.xpath('//span[@id="domcache_project"]/@data-propertytype').extract_first()
        except:
            project_type = None
        try:
            project_id = response.xpath('//span[@id="domcache_project"]/@data-psmid').extract_first()
        except:
            project_id = None
        try:
            latitude = response.xpath('//span[@id="domcache_project"]/@data-psmlat').extract_first()
        except:
            latitude = None
        try:
            longitude = response.xpath('//span[@id="domcache_project"]/@data-psmlongt').extract_first()
        except:
            longitude = None
        try:
            min_price = response.xpath('//span[@id="domcache_project"]/@data-minprice').extract_first()
        except:
            min_price = None
        try:
            max_price = response.xpath('//span[@id="domcache_project"]/@data-maxprice').extract_first()
        except:
            max_price = None
        try:
            proj_bhk = str(response.xpath('//span[@id="domcache_project"]/@data-bd').extract_first().split(','))
        except:
            proj_bhk = None
        try:
            proj_area = response.xpath('//div[contains(text(),"Project Size")]/following-sibling::div/text()').extract_first()
        except:
            proj_area = None
        try:
            proj_launch_dt = response.xpath('//div[contains(text(),"Launch Date")]/following-sibling::div/text()').extract_first()
        except:
            proj_launch_dt = None
        try:
            proj_units_ct = response.xpath('//div[contains(text(),"Total Units")]/following-sibling::div/text()').extract_first()
        except:
            proj_units_ct = None
        try:
            proj_towers_ct = response.xpath('//div[contains(text(),"Total Towers")]/following-sibling::div/text()').extract_first()
        except:
            proj_towers_ct = None
        try:
            proj_area = response.xpath('//div[contains(text(),"Project Size")]/following-sibling::div/text()').extract_first()
        except:
            proj_area = None
        try:
            possession_by = response.xpath('//*[contains(text(),"Possession by")]/text()').extract_first()
        except:
            possession_by = None
        try:
            amenities = str([c.strip() for c in response.xpath('//div[@class="amenities"]/div[@class="amenities__item "]/span/text()').extract()])
        except:
            amenities = None
        
        with open(filename, 'a') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow([project_id,project_name,locality,city,project_type,project_developer,latitude,longitude,min_price,max_price,proj_bhk,proj_area,proj_launch_dt,possession_by,proj_units_ct,proj_towers_ct,proj_area,amenities])
            
            
    
        yield {'pg_no':pg_no,'city_name':city_name}
        
        

    def errback_httpbin(self, failure):
        # log all failures
        self.logger.error(repr(failure))

        # in case you want to do something special for some errors,
        # you may need the failure's type:

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error("HttpError on %s", response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error("DNSLookupError on %s", request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error("TimeoutError on %s", request.url)