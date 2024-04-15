import requests
from bs4 import BeautifulSoup
import re
import time

def convert2int(string):
    str_list = [ord(c) for c in string]
    return sum(str_list)

def unique_list(input_list):
    list_set = set(input_list)
    unique_list = (list(list_set))
    return unique_list

def extract_ad_data(link):
    time.sleep(20)
    ad = requests.get("https://divar.ir%s" % link, stream=True)
    ad_soup = BeautifulSoup(ad.text, "html.parser")
    ad_info = ad_soup.find_all("section")
    #print(ad.text)

    # Get location
    try:
        location_info = ad_info[0].find("div", attrs={'class': 'kt-page-title__subtitle'})
        location = re.findall(r'\S*، (.*)',location_info.text)[0]

        # Get attributes
        attributes = []
        tables = ad_info[0].find_all("table")
        for table in tables:
            tds = table.find_all("td", attrs={'class': 'kt-group-row-item__value'})
            for td in tds:
                attributes.append(td.text)
    
        # Get price and floor
        rows_data = ad_info[0].find_all("div", attrs={'class': 'kt-base-row kt-base-row--large kt-unexpandable-row'})
        for row in rows_data:
            if bool(re.search(r'قیمت کل', row.text)):
                price = re.findall(r'(\d+)', re.sub('٬','',row.text))[0].strip()
            elif bool(re.search(r'طبقه', row.text)):
                t = re.findall(r'(\d+)', row.text)
                floor = t[0] if len(t) > 0 else 0
    
        # Create dictionary
        ad_attributes = {
            'location': location,
            'metraj': int(attributes[0]),
            'sakht': int(attributes[1]),
            'otagh': int(attributes[2]),
            'asansor': not bool(re.search(r'ندارد', attributes[3])),
            'parking': not bool(re.search(r'ندارد', attributes[4])),
            'anbari': not bool(re.search(r'ندارد', attributes[5])),
            'price': int(price)/1000,
            'floor': int(floor)
        }
    except:
        ad_attributes = {}
    return ad_attributes
