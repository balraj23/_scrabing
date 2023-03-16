from bs4 import BeautifulSoup
import requests
import csv
from selenium import webdriver

def get_url(search_term):
    template = "https://www.amazon.com/s?k={}&ref=nb_sb_noss"
    search_term = search_term.replace(' ','+')
    
    url = template.format(search_term)
    url += '&page{}'
    return url

def extract_record(item):
    atag = item.h2.a
    description = atag.text.strip()
    url = "https://www.amazon.com" + atag.get('href')

    try:
        price_parent = item.find('span','a-price')
        price = price_parent.find('span','a-offscreen').text
    except AttributeError:
        return 
    
    try:
        rating = item.find('span',{'class':'a-size-base'}).text
        review_count = item.find('span',{'class':'a-size-base s-underline-text'}).text
    except AttributeError:
        rating = ''
        review_count = ''
    result = (description,price,rating,review_count,url)
    return result

def main(search_term):
    driver = webdriver.Chrome(executable_path="/home/palraj/chromedriver_linux64/chromedriver.exe")

    record = []
    url = get_url(search_term)
    
    with open('re.csv','w',newline='',encoding='utf-8') as  f:
        writer = csv.writer(f)
        writer.writerow(['description','price','rating','reviewcount','url'])

        for page in range(1,3):
            driver.get(url.format(page))
            soup = BeautifulSoup(driver.page_source,'html.parser')
            results = soup.find_all('div',{"data-component-type":'s-search-result'})
        
            for item in results:
                record = extract_record(item)
                if record:
                    # records.append(record)
                    writer.writerow(record)
                
    driver.close()
    
main('boat')