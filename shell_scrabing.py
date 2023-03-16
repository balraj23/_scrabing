from bs4 import BeautifulSoup
import requests
import csv
from selenium import webdriver

def get_url(search_term):
    template = f"https://www.shell.in/motorists/oils-lubricants/{search_term}.html"
    search_term = search_term.replace(' ','+')
    
    url = template.format(search_term)
    print(url)
    return url

def extract_record(item):
    atag = item.h3.a
    print(atag)
    name = atag.text.strip()
    url = "https://www.shell.in" + atag.get('href')
    result = (name,url)
    return result


def main(search_term):
    driver = webdriver.Chrome(executable_path="/home/palraj/chromedriver_linux64/chromedriver.exe")

    record = []
    url = get_url(search_term)
    
    with open('res.csv','w',newline='',encoding='utf-8') as  f:
        writer = csv.writer(f)
        writer.writerow(['name','url'])
        driver.get(url)
        soup = BeautifulSoup(driver.page_source,'html.parser')
        results = soup.find_all('div',{"data-ast-meta":'list-item'})
    
        for item in results:
            print("for")
            record = extract_record(item)
            if record:
                # records.append(record)
                writer.writerow(record)
                
    driver.close()

main('helix-for-cars')