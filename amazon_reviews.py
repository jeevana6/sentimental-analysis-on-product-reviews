
import re
from lxml import html
from json import dump,loads
from requests import get
import json
from re import sub
from dateutil import parser as dateparser
from time import sleep
from jsontocsv_data import json_to_csv

class Amazon(object):
    def __init__(self):
        self.review_data = []
        self.rating_data = []
        self.data=[]
        taken_input=input("enter product id : ")
        self.AsinList=[taken_input]
        self.ReadAsin()
        self.Revrate()
        json_to_csv()
        '''if json_to_csv():
            print("true")'''

    def ParseReviews(self,asin):
        # This script has only been tested with Amazon.com
        amazon_url  = 'http://www.amazon.com/dp/'+asin
        # Add some recent user agent to prevent amazon from blocking the request
        # Find some chrome user agent strings  here https://udger.com/resources/ua-list/browser-detail?browser=Chrome
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
        #https: // www.amazon.com / dp / B07DNMHBRC / ref = sspa_dk_detail_2?psc = 1 & pd_rd_i = B07DNMHBRC & pd_rd_wg = 70Lx2 & pd_rd_r = 30WME7MF7PT99664YZC9 & pd_rd_w = Vf2js & smid = A12LTVP7KBAA4
        for i in range(5):
            response = get(amazon_url, headers = headers, verify=False, timeout=30)
            if response.status_code == 404:
                return {"url": amazon_url, "error": "page not found"}
            if response.status_code != 200:
                continue
        
            # Removing the null bytes from the response.
            cleaned_response = response.text.replace('\x00', '')
        
            parser = html.fromstring(cleaned_response)
            XPATH_AGGREGATE = '//span[@id="acrCustomerReviewText"]'
            XPATH_REVIEW_SECTION_1 = '//div[contains(@id,"reviews-summary")]'
            XPATH_REVIEW_SECTION_2 = '//div[@data-hook="review"]'
            XPATH_AGGREGATE_RATING = '//table[@id="histogramTable"]//tr'
            XPATH_PRODUCT_NAME = '//h1//span[@id="productTitle"]//text()'
            XPATH_PRODUCT_PRICE = '//span[@id="priceblock_ourprice"]/text()'

            raw_product_price = parser.xpath(XPATH_PRODUCT_PRICE)
            raw_product_name = parser.xpath(XPATH_PRODUCT_NAME)
            total_ratings  = parser.xpath(XPATH_AGGREGATE_RATING)
            reviews = parser.xpath(XPATH_REVIEW_SECTION_1)

            product_price = ''.join(raw_product_price).replace(',', '')
            product_name = ''.join(raw_product_name).strip()

            if not reviews:
                reviews = parser.xpath(XPATH_REVIEW_SECTION_2)
            ratings_dict = {}
            reviews_list = []

            # Grabing the rating  section in product page
            for ratings in total_ratings:
                extracted_rating = ratings.xpath('./td//a//text()')
                if extracted_rating:
                    rating_key = extracted_rating[0]
                    raw_raing_value = extracted_rating[1]
                    rating_value = raw_raing_value
                    if rating_key:
                        ratings_dict.update({rating_key: rating_value})
        
            # Parsing individual reviews
            for review in reviews:
                XPATH_RATING  = './/i[@data-hook="review-star-rating"]//text()'
                XPATH_REVIEW_HEADER = './/a[@data-hook="review-title"]//text()'
                XPATH_REVIEW_POSTED_DATE = './/span[@data-hook="review-date"]//text()'
                XPATH_REVIEW_TEXT_1 = './/div[@data-hook="review-collapsed"]//text()'
                XPATH_REVIEW_TEXT_2 = './/div//span[@data-action="columnbalancing-showfullreview"]/@data-columnbalancing-showfullreview'
                XPATH_REVIEW_COMMENTS = './/span[@data-hook="review-comment"]//text()'
                XPATH_AUTHOR = './/span[contains(@class,"profile-name")]//text()'
                XPATH_REVIEW_TEXT_3 = './/div[contains(@id,"dpReviews")]/div/text()'
            
                raw_review_author = review.xpath(XPATH_AUTHOR)
                raw_review_rating = review.xpath(XPATH_RATING)
                raw_review_header = review.xpath(XPATH_REVIEW_HEADER)
                raw_review_posted_date = review.xpath(XPATH_REVIEW_POSTED_DATE)
                raw_review_text1 = review.xpath(XPATH_REVIEW_TEXT_1)
                raw_review_text2 = review.xpath(XPATH_REVIEW_TEXT_2)
                raw_review_text3 = review.xpath(XPATH_REVIEW_TEXT_3)

                # Cleaning data
                author = ' '.join(' '.join(raw_review_author).split())
                review_rating = ''.join(raw_review_rating).replace('out of 5 stars', '')
                review_header = ' '.join(' '.join(raw_review_header).split())

                try:
                    review_posted_date = dateparser.parse(''.join(raw_review_posted_date)).strftime('%d %b %Y')
                except:
                    review_posted_date = None
                review_text = ' '.join(' '.join(raw_review_text1).split())

                # Grabbing hidden comments if present
                if raw_review_text2:
                    json_loaded_review_data = loads(raw_review_text2[0])
                    json_loaded_review_data_text = json_loaded_review_data['rest']
                    cleaned_json_loaded_review_data_text = re.sub('<.*?>', '', json_loaded_review_data_text)
                    full_review_text = review_text+cleaned_json_loaded_review_data_text
                else:
                    full_review_text = review_text
                if not raw_review_text1:
                    full_review_text = ' '.join(' '.join(raw_review_text3).split())

                raw_review_comments = review.xpath(XPATH_REVIEW_COMMENTS)
                review_comments = ''.join(raw_review_comments)
                review_comments = sub('[A-Za-z]', '', review_comments).strip()
                review_dict = {
                                    'review_comment_count': review_comments,
                                    'review_text': full_review_text,
                                    'review_posted_date': review_posted_date,
                                    'review_header': review_header,
                                    'review_rating': review_rating,
                                    'review_author': author

                                }
                reviews_list.append(review_dict)

            data = {
                        'ratings': ratings_dict,
                        'reviews': reviews_list,
                        'url': amazon_url,
                        'name': product_name,
                        'price': product_price
                
                    }
            return data

        return {"error": "failed to process the page", "url": amazon_url}
            

    def ReadAsin(self):
        # Add your own ASINs here
        #AsinList = ['B01ETPUQ6E', 'B017HW9DEW', 'B00U8KSIOM']
        #self.AsinList=[id]
        extracted_data = []
    
        for asin in self.AsinList:
            print("Downloading and processing page http://www.amazon.com/dp/" + asin)
            extracted_data.append(self.ParseReviews(asin))
            sleep(5)
        f = open('data.json', 'w')
        dump(extracted_data, f, indent=4)
        f.close()




    def Revrate(self):
        with open('data.json') as json_file:
            self.data=json.load(json_file)
            for p in self.data:
                self.rating_data.append(p['ratings'])
            #print(self.rating_data)
            for q in self.data:
                #review_data.append(q['reviews']['review_text'])
                m=q['reviews']
                for n in m:
                    self.review_data.append(n['review_text'])
            #print(self.review_data)
            print('loading of data finshed')
            return self.review_data,self.rating_data

    '''if __name__ == '__main__':
        self.ReadAsin()
        self.Revrate()'''


    



