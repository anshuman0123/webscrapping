import sys
from bs4 import BeautifulSoup
import requests
import pandas as pd

# key_word = "restaurant"
# location = "Warner+Robins%2C+GA"
key_word = sys.argv[1]
location = sys.argv[2]
url = f'https://www.yellowpages.com/search?search_terms={key_word}&geo_location_terms={location}'
r = requests.get(url)
html_content = r.content
soup = BeautifulSoup(html_content, 'html.parser')
anchors = soup.find_all('a', class_='business-name')
address1 = soup.find_all('div', class_='street-address')
address2 = soup.find_all('div', class_='locality')
website = soup.find_all('a', class_='track-visit-website')
name_list = []
for a in anchors:
    name_list.append(a.find_next('span').text)
final_address = []
for i in range(len(address1)):
    final_address.append(address1[i].text + ", " + address2[i].text)
# print(final_address)
website_list = []
for w in website:
    website_list.append(w.get('href'))
depth = min(len(name_list), len(final_address), len(website_list))

a = {'Name': name_list[:depth], 'Address': final_address[:depth], 'Website': website_list[:depth]}
df = pd.DataFrame(a)
df.to_csv('data.csv')
