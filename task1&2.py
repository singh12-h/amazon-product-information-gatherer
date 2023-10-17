import requests
from bs4 import BeautifulSoup
import csv

# Part 1: Scraping Product Listings

# Initialize a list to store the data
data = []

# Loop through 20 pages
for page_num in range(1, 21):
    url = f'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_{page_num}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    products = soup.find_all('div', class_='s-result-item')

    for product in products:
        product_url_element = product.find('a', class_='s-no-outline')
        product_name_element = product.find('span', class_='a-text-normal')
        product_price_element = product.find('span', class_='a-price-whole')
        product_rating_element = product.find('span', class_='a-icon-alt')
        num_reviews_element = product.find('span', class_='a-size-base')

        if all((product_url_element, product_name_element, product_price_element, product_rating_element, num_reviews_element)):
            product_url = f"https://www.amazon.in{product_url_element.get('href')}"
            product_name = product_name_element.string
            product_price = product_price_element.string
            product_rating = product_rating_element.string
            num_reviews = num_reviews_element.string

            data.append({
                'Product URL': product_url,
                'Product Name': product_name,
                'Product Price': product_price,
                'Rating': product_rating,
                'Number of Reviews': num_reviews
            })

# Part 2: Scraping Product Details

for item in data:
    url = item['Product URL']
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    description = soup.find('span', id='productTitle')
    asin = soup.find('th', string='ASIN')
    product_description = soup.find('div', id='productDescription')
    manufacturer = soup.find('div', class_='detailBulletsWrapper_feature_div')

    if description:
        item['Description'] = description.string.strip()

    if asin:
        item['ASIN'] = asin.find_next('td').string.strip()

    if product_description:
        item['Product Description'] = product_description.string.strip()

    if manufacturer:
        item['Manufacturer'] = manufacturer.find('span', class_='a-declarative').string.strip()

# Export data to CSV
with open('amazon_products.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Product URL', 'Product Name', 'Product Price', 'Rating', 'Number of Reviews', 'Description', 'ASIN', 'Product Description', 'Manufacturer']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for item in data:
        writer.writerow(item)
