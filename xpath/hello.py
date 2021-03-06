# import sys
# # Takes first name and last name via command
# # line arguments and then display them
# print("Output from Python")
# print("First name: " + sys.argv[1])
# print("Last name: " + sys.argv[2])




from lxml import html
import csv,os,json
import requests
from builtins import ValueError
from time import sleep

def AmzonParser(url):
    headers = {'User-Agent': 'Chrome/42.0.2311.90 Safari/537.36'}
    page = requests.get(url,headers=headers)
    #   tree = html.fromString(page.content)
    while True:
        sleep(3)
        try:
            doc = html.fromstring(page.content)
            XPATH_NAME = '//h1[@id="title"]//text()'
            XPATH_SALE_PRICE = '//span[contains(@id,"ourprice") or contains(@id,"saleprice")]/text()'
            XPATH_RATINGS = '//i[@class="a-icon a-icon-star a-star-4-5"]//text()'
            XPATH_ORIGINAL_PRICE = '//td[contains(text(),"List Price") or contains(text(),"M.R.P") or contains(text(),"Price")]/following-sibling::td/text()'
            XPATH_CATEGORY = '//a[@class="a-link-normal a-color-tertiary"]//text()'
            XPATH_AVAILABILITY = '//div[@id="availability"]//text()'
            #XPATH_CONTENT = '//div[@id="bookDescription_feature_div"]//noscript//text()'
            XPATH_CONTENT = '//div[@id="bookDescription_feature_div"]//noscript//text()'


            RAW_NAME = doc.xpath(XPATH_NAME)
            RAW_SALE_PRICE = doc.xpath(XPATH_SALE_PRICE)
            RAW_RATINGS = doc.xpath(XPATH_RATINGS)
            RAW_CATEGORY = doc.xpath(XPATH_CATEGORY)
            RAW_ORIGINAL_PRICE = doc.xpath(XPATH_ORIGINAL_PRICE)
            RAw_AVAILABILITY = doc.xpath(XPATH_AVAILABILITY)
            RAW_CONTENT = doc.xpath(XPATH_CONTENT)

            print(RAW_NAME);

            NAME = ' '.join(''.join(RAW_NAME).split()) if RAW_NAME else None
            SALE_PRICE = ' '.join(''.join(RAW_SALE_PRICE).split()).strip() if RAW_SALE_PRICE else None
            CATEGORY = ' > '.join([i.strip() for i in RAW_CATEGORY]) if RAW_CATEGORY else None
            ORIGINAL_PRICE = ''.join(RAW_ORIGINAL_PRICE).strip() if RAW_ORIGINAL_PRICE else None
            AVAILABILITY = ''.join(RAw_AVAILABILITY).strip() if RAw_AVAILABILITY else None
            CONTENT = ''.join(RAW_CONTENT).strip() if RAW_CONTENT else None
            RATINGS = ' '.join(RAW_RATINGS).strip() if RAW_RATINGS else None

            if not ORIGINAL_PRICE:
                ORIGINAL_PRICE = SALE_PRICE

            if page.status_code!=200:
                raise ValueError('captha')
            data = {
                    'NAME':NAME,
                    'SALE_PRICE':SALE_PRICE,
                    'RATINGS' : RAW_RATINGS,
                    'CATEGORY':CATEGORY,
                    'ORIGINAL_PRICE':ORIGINAL_PRICE,
                    'AVAILABILITY':AVAILABILITY,
                    'URL':url,
                    'CONTENT': CONTENT
                    }

            return data
        except Exception as e:
            print(e)

def ReadAsin(asin):
    # AsinList = csv.DictReader(open(os.path.join(os.path.dirname(__file__),"Asinfeed.csv")))
    AsinList = [str(asin)]
    extracted_data = []
    for i in AsinList:
        url = "http://www.amazon.com/dp/"+i
        print("Processing: "+url)
        extracted_data.append(AmzonParser(url))
        sleep(5)
    f=open('data.json','w')
    json.dump(extracted_data,f,indent=4)
    f.close()


import sys
if __name__ == "__main__":

	ReadAsin(sys.argv[1])
