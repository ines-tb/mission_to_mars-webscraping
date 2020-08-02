# %%
# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd


# %%
# Set the executable path and initialize the chrome browser in splinter
executablePath = {'executable_path': 'chromedriver'}
browser = Browser('chrome', **executablePath)


# %%
# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


# %%
html = browser.html
newsSoup = soup(html, 'html.parser')
slideElem = newsSoup.select_one('ul.item_list li.slide')


# %%
# News title object object
slideElem.find("div", class_='content_title')


# %%
# Use the parent element to find the first `a` tag and save it as `news_title`
newsTitle = slideElem.find("div", class_='content_title').get_text()



# %%
# Use the parent element to find the paragraph text
newsP = slideElem.find('div', class_="article_teaser_body").get_text()


# %% [markdown]
# ## Featured Images

# %%
# Visit URL
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)


# %%

# Find and click the full image button
fullImageElem = browser.find_by_id('full_image')
fullImageElem.click()


# %%
# Find the more info button and click that
browser.is_element_present_by_text('more info', wait_time=1)
moreInfoElem = browser.links.find_by_partial_text('more info')
moreInfoElem.click()


# %%
# Parse the resulting html with soup
html = browser.html
imgSoup = soup(html, 'html.parser')


# %%
# Find the relative image url
imgUrlRel = imgSoup.select_one('figure.lede a img').get("src")



# %%
# Use the base URL to create an absolute URL
imgUrl = f"https://www.jpl.nasa.gov{imgUrlRel}"



# %%
df = pd.read_html('http://space-facts.com/mars/')[0]
df.columns=['description', 'value']
df.set_index('description', inplace=True)


# %%
df.to_html()


# %%
browser.quit()




