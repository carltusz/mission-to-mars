#import splinter and beautiful soup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt



def scrape_all():
    #set up splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)
    
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres": mars_images(browser)
            
    }
    
    # stop webdriver and return data
    browser.quit()
    return data



#create function
def mars_news(browser):
    #visit the mars nasa news site
    url='https://redplanetscience.com'
    browser.visit(url)
    #optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # article scraping
    html = browser.html
    news_soup = soup(html, 'html.parser')
    
    #error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # use parent element to find the first 'a' tag and save it as 'new_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # use parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    except AttributeError:
        return None, None
    
    return news_title, news_p


# Image Scraping

def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    
    # error handling
    try:
        # find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    except AttributeError:
        return None
    
    # use the base url to create an absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    return img_url


def mars_facts():
    # add try/except for error handling
    try:
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None

    # assing columns and set index of dataframe
    df.columns=['description', 'Mars','Earth']
    df.set_index('description',inplace=True)
    
    # convert dataframe into HTML format, add bootstrap
    return df.to_html(classes=["table", "table-striped"])


def mars_images(browser):
    #set up splinter
    #executable_path = {'executable_path': ChromeDriverManager().install()}
    #browser = Browser('chrome', **executable_path, headless=True)
    
    #visit image webset
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    
    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    html = browser.html
    hemi_soup = soup(html, 'html.parser')
    hemi_box = hemi_soup.find_all('div', class_='description')

    for item in hemi_box:

        #create empty dictionary for results
        hemisphere = {}
        
        # get title from link 
        title = item.find('h3').text
        
        #visit URL to get full size images using title to match text
        browser.click_link_by_partial_text(title)
        html=browser.html
        
        # get the URL for full size images
        img_soup = soup(html, 'html.parser')
        img_src = img_soup.find('a',  text="Sample")['href']
        
        # append description and url to list
        hemisphere = {"img_url":url+img_src, "title":title}
        hemisphere_image_urls.append(hemisphere)
        
        print(title)
        
        #return to root URL
        browser.back()
    
    #exit browser
    browser.quit()
    
    return hemisphere_image_urls


if __name__ == "__main__":
    # if running as script, print scraped data
    print(scrape_all())