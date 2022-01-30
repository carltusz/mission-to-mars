#!/usr/bin/env python
# coding: utf-8



# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager




# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)




### Visit the NASA Mars News Site

# Visit the mars nasa news site
url = 'https://redplanetscience.com/'
browser.visit(url)




# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)




# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')

slide_elem.find('div', class_='content_title')



# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title



# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p




### JPL Space Images Featured Image

# Visit URL
url = 'https://spaceimages-mars.com'
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
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url



### Mars Facts

df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.head()




df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df



df.to_html()


# D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

### Hemispheres

# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)
print(url)



# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []



# 3. Write code to retrieve the image urls and titles for each hemisphere.
html = browser.html
hemi_soup = soup(html, 'html.parser')

hemi_box = img_soup.find_all('div', class_='description')

#browser.click_link_by_partial_text(new_link.text)
#browser.visit(url + extension)

for item in img_box:

    #create empty dictionary for results
    hemisphere = {}
    
    # get title and URL from img_box 
    title = item.find('h3').text
    extension = item.find('a', class_="itemLink", href=True)['href']
    
    #visit URL to get full size images
    browser.click_link_by_partial_text(title)
    html=browser.html
    
    #print HTML for debugging
    #print("----------------------")
    #print(title)
    #print("----------------------")
    #print(html)
    
    
    img_soup = soup(html, 'html.parser')
    img_src = img_soup.find('a',  text="Sample")['href']
    
    # append description and url to list
    hemisphere = {"img_url":url+img_src, "title":title}
    hemisphere_image_urls.append(hemisphere)
    
    #return to root URL
    browser.back()
    
#print list for debugging
#print(hemisphere_image_urls)


# In[128]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[129]:


# 5. Quit the browser
browser.quit()

