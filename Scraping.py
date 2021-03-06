#!/usr/bin/env python
# coding: utf-8

# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt

def scrape_all():
   # Initiate headless driver for deployment
   #browser = Browser("chrome", executable_path="C:/Webdrivers/chromedriver.exe", headless=True)
   browser = Browser("chrome", executable_path="chromedriver.exe", headless=True)
   
   news_title, news_paragraph = mars_news(browser)
   
   # Run all scraping functions and store results in dictionary
   data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "hemispheres" : mars_hemis(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
   }
   # Stop webdriver and return data
   browser.quit()
   return data 

# Set the executable path and initialize the chrome browser in splinter
#executable_path = {'executable_path': 'C:/Webdrivers/chromedriver.exe'}
#browser = Browser('chrome', **executable_path)

def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1) # 1 second delay

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('ul.item_list li.slide') 
        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find("div", class_='content_title').get_text()
        
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
    except AttributeError:
        return None, None
    return news_title, news_p


def featured_image(browser):
    # ## JPL Space Images Featured Image
    # Visit URL
    # in case of error we have to run the second cell from the top
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    # Find and click the full image button- this will return the second button on the web page
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    try: 
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    except AttributeError:
        return None 
    # Use the base URL to create an absolute URL
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
    return img_url

def mars_facts():
    # ## Mars Facts

    # Below: The Pandas function read_html() specifically searches for and returns a list of tables found in the HTML. By specifying an index of 0, we're telling Pandas to pull only the first table it encounters, or the first item in the list. Then, it turns the table into a DataFrame.
    try:
      # use 'read_html" to scrape the facts table into a dataframe
      df = pd.read_html('http://space-facts.com/mars/')[0]
    except BaseException:
      return None
    
    # Assign columns and set index of dataframe
    df.columns=['description', 'value']
    df.set_index('description', inplace=True)
    
    # converting a data frame to html table
    return df.to_html()

def mars_hemis(browser):
    # Mars Hemispheres urls and images
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    hemisphere_image_urls = []
    #hemispheres = {}
    html = browser.html
    image_soup = soup(html,'html.parser')
    
    image_titles = image_soup.find_all('h3')
    
    for title in image_titles:
        hemispheres = {}
        hemispheres['title']=title.text
        
        # find the image for each hemisphere
        browser.visit(url)
        browser.links.find_by_partial_text(title.text).click()
        try:
            image_soup = soup(browser.html,'html.parser')
        except AttributeError:
            return None 
        image_url = image_soup.find('div', class_="downloads")
        image_url = image_url.find('a')['href']
        hemispheres['img_url'] = image_url
        
        hemisphere_image_urls.append(hemispheres)
    
    return hemisphere_image_urls

if __name__ == "__main__":
    # If running as script, print scraped data
    print("-----" , scrape_all())


