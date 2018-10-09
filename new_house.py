import requests
from bs4 import BeautifulSoup
import pandas as pd

soup = BeautifulSoup(c, "html.parser")
data = soup.find_all("li",{"class":"search-results__listing"}) #get dataset of content needed
total_pages = int(soup.find_all("a",{"class":"paginator__page-button"})[-1].text) #find total number of pages in above search


url = "https://www.domain.com.au/rent/west-perth-wa-6005/?ssubs=1"
for page in range(1,5):
    r = requests.get(url+"&page="+str(page))
    c = r.content #download content of webpage

    soup = BeautifulSoup(c, "html.parser")
    data = soup.find_all("li",{"class":"search-results__listing"}) #get dataset of content needed

    df_list = [] #list to create dataframe from dictionaries

    for item in data:
        d = {} #dictionary to store iterations
        try:
            d['Price'] = item.find("p",{"class":"listing-result__price"}).text #price data
            d['Address'] = item.find("a" ,{"class":"address is-two-lines listing-result__address"}).text #address
            d['Beds'] = item.find_all("span" ,{"class":"property-feature__feature"})[0].text #number of beds
            d['Baths'] = item.find_all("span" ,{"class":"property-feature__feature"})[1].text #number of baths
            d['Parking'] = item.find_all("span" ,{"class":"property-feature__feature"})[2].text #number of parking bays
            d['Link'] = item.find("a", {"class":"address is-two-lines listing-result__address"}).get('href') #link address
        except:
            pass
        df_list.append(d)

data_frame = pd.DataFrame(df_list)
data_frame.to_csv('houselist.csv')
