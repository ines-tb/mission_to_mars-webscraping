# %%
# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd


# Set the executable path and initialize the chrome browser in splinter
executablePath = {'executable_path': 'chromedriver'}
browser = Browser('chrome', **executablePath)


def marsNews(browser):

    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    html = browser.html
    newsSoup = soup(html, 'html.parser')
    
    # Add try/except for error handling
    try:
        slideElem = newsSoup.select_one('ul.item_list li.slide')
        # Use the parent element to find the first `a` tag and save it as `news_title`
        newsTitle = slideElem.find("div", class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        newsP = slideElem.find('div', class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None

    return newsTitle, newsP


def featuredImage(browser):
    
    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find and click the full image button
    fullImageElem = browser.find_by_id('full_image')
    fullImageElem.click()

    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    moreInfoElem = browser.links.find_by_partial_text('more info')
    moreInfoElem.click()

    # Parse the resulting html with soup
    html = browser.html
    imgSoup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        imgUrlRel = imgSoup.select_one('figure.lede a img').get("src")
        
    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    imgUrl = f"https://www.jpl.nasa.gov{imgUrlRel}"

    return imgUrl


def marsFacts():
    
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]
    except BaseException:
        return None
    
    # Assign columns and set index of dataframe
    df.columns=['description', 'value']
    df.set_index('description', inplace=True)
    
    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()


browser.quit()




