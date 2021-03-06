#!/usr/bin/env python
# coding: utf-8




# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd




# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path)

# ### Visit the NASA Mars News Site

# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('ul.item_list li.slide')

slide_elem.find("div", class_='content_title')

# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p

# ### JPL Space Images Featured Image

# Visit URL
url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup

# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# Use the base url to create an absolute url
img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
img_url


# ### Mars Facts
df = pd.read_html('http://space-facts.com/mars/')[0]
df.head()

df.columns=['Description', 'Mars']
df.set_index('Description', inplace=True)
df
df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres



# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)




# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []
hemisphere = {}
html = browser.html
image_soup = soup(html,'html.parser')

image_titles = image_soup.find_all('h3')
for title in image_titles:
    hemisphere = {}
    hemisphere['title']=title.text
    
    # find the image for each hemisphere
    browser.visit(url)
    browser.links.find_by_partial_text(title.text).click()
    image_soup = soup(browser.html,'html.parser')
    image_url = image_soup.find('div', class_="downloads")
    image_url = image_url.find('a')['href']
    hemisphere['img_url'] = image_url
    
    hemisphere_image_urls.append(hemisphere)
    


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls




# 5. Quit the browser
browser.quit()






