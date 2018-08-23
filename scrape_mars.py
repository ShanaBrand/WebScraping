from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import pymongo
import pandas as pd

executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)


conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn);

def scrape():

    nasa_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    mw_url = 'https://twitter.com/marswxreport?lang=en'
    mf_url = 'https://space-facts.com/mars/'
    mh_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    nasa_resp = requests.get(nasa_url)
    jpl_resp = requests.get(jpl_url)
    mw_resp = requests.get(mw_url)
    mf_resp = requests.get(mf_url)
    mh_resp = requests.get(mh_url)

##NASA MARS NEWS
        #Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text.
        #Assign the text to variables that you can reference later.
    n_soup = bs(nasa_resp.text,'html.parser')
    print(n_soup.prettify())
    
    news_title = n_soup.find_all('div',class_='content_title')
    for n in news_title:
        print("TITLE ", n.text)
        title = n.text
        
    news_para = n_soup.find_all('div',class_='rollover_description_inner')       
    for p in news_para:
        paragraph = p.text
        print("PARAGRAPH", p.text) 

##JPL Featured Image
        ##Use splinter to navigate the site and find the image url for the current Featured Mars Image and 
        #assign the url string to a variable called featured_image_url.
        #Make sure to find the image url to the full size .jpg image.
        #Make sure to save a complete url string for this image.
    browser.visit(jpl_url)
    jpl_html = browser.html
    j_soup = bs(jpl_html,'lxml')
    
    ft_img = j_soup.find('article', class_='carousel_item')['style'][23:75]
    ft_img_url = jpl_url+ft_img
    ft_img_url 

##MARS Weather Twitter
        #Visit the Mars Weather twitter account here and scrape the latest Mars weather tweet from the page. 
        #Save the tweet text for the weather report as a variable called mars_weather.
    mw_soup= bs(mw_resp.text,'lxml')
    print(mw_soup)
    tweet = mw_soup.find_all('div',class_="js-tweet-text-container")
    mars_weather = tweet[0].text



##MARS Facts Table
    #Visit the Mars Facts webpage here and use Pandas to scrape the table containing facts about the planet including
    #Diameter, Mass, etc.
    #Use Pandas to convert the data to a HTML table string.

    fact_tbl = pd.read_html(mf_url)
    fact_tbl

    df_tbl = fact_tbl[0]
    df_tbl


#MARS HEMISPHERE
        # Visit the USGS Astrogeology site here to obtain high resolution images for each of Mar's hemispheres.
        # You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
        # Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing
        # the hemisphere name. Use a Python dictionary to store the data using the keys img_url and title.
        # Append the dictionary with the image url string and the hemisphere title to a list.
        # This list will contain one dictionary for each hemisphere.
    
    mh_soup = bs(mh_resp.text,'lxml')
        
    hem_dic = {}
    names = []
    full_img = []
    myList = []

    baseurl = 'https://astrogeology.usgs.gov'
        
    items = mh_soup.find_all('div', class_='item')

    for t in items:
        title = t.find('h3').text
        names.append(title)
        hem_dic.update({'title':(title)})

    
    for i in items:
        links = i.find('a', href=True)
        found = links['href']
        url = baseurl + found
        browser.visit(url)


        dwn_soup = bs(browser.html,'lxml')
        dwn_section = dwn_soup.find('div', class_='downloads')
        img_links = dwn_section.find('a', href=True)
        img_url = img_links['href']
        full_img.append(img_url) 

        hem_dic.update({'img_url':(img_url)})

            
    myList.append(hem_dic)


    print(myList)

        
    

