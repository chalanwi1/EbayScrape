import requests
import pandas as pd
from bs4 import BeautifulSoup

# url of web page being scraped
page = requests.get('https://www.ebay.com/deals')

# Parse web page with beautiful soup
soup = BeautifulSoup(page.content, 'html.parser')

# Get container with all featured items
deals = soup.find_all('div', 'ebayui-dne-item-featured-card')

# Get all items in featured container
items = deals[0].find_all('div', 'dne-itemtile dne-itemtile-medium')

# Data points being scraped
# Empty list, uses for loop below and appends each price
prices = []
# Uses list comprehension
product_name = [item.find('h3').get('title') for item in items]
links = [item.find('a').get('href') for item in items]

# Loop through each item in deals
for item in items:
    # add product price to prices list if item has price
    if item.find('div', 'dne-itemtile-price'):
        prices.append(item.find('div', 'dne-itemtile-price').text)
    else:
        prices.append('NA')

# Store data points scraped in pandas data frame
final_deals = pd.DataFrame(
    {
        'Title': product_name,
        'Price': prices,
        'Links': links,
    }
)

# Increment item count by 1 for title columns
final_deals.index += 1
# Write data to csv file
final_deals.to_csv('ebay_deals.csv')
