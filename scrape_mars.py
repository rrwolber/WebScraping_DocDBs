from bs4 import BeautifulSoup as bs
import requests
import cssutils
import pandas as pd

def scrape():

    mars_data = {}


    #retrieve new mars news
    news = {}
    mars_news = requests.get("https://mars.nasa.gov/news/")
    soup = bs(mars_news.text, 'html.parser')
    topNews = soup.find("div", class_="image_and_description_container")

    news_p = topNews.find("div", class_="rollover_description_inner").text
    news_title = topNews.find_all("img")[1]
    news_title = news_title.get("alt","")


    mars_data["news_title"] = news_title
    mars_data["news_p"] = news_p



    #retrieve jpl featured image
    jpl = requests.get("https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars")
    jplsoup = bs(jpl.text, 'html.parser')
    featured = jplsoup.find("div", id="page")
    featured = featured.find("article")
    featured = featured.get("style")
    style = cssutils.parseStyle(featured)
    url = style['background-image']
    url = url.replace('url(', '').replace(')', '')
    featured_image_url = "https://www.jpl.nasa.gov" + url

    mars_data["featured_image"] = featured_image_url



    #retrieve most recent mars weather
    weather = requests.get("https://twitter.com/marswxreport?lang=en")
    wsoup = bs(weather.text, "html.parser")

    latest = wsoup.find('div', {'class': 'ProfileTimeline'})
    latest = latest.find("p", {'class': "TweetTextSize TweetTextSize--normal js-tweet-text tweet-text"})
    mars_weather = latest.text

    mars_data["weather"] = mars_weather



    #retrieve mars fact table
    facts = requests.get("https://space-facts.com/mars/")
    fsoup = bs(facts.text, "html.parser")

    def souptable(table):
        for row in table.find_all('tr'):
            yield [col.text for col in row.find_all('td')]

    table = fsoup.find("table")
    mf_df = pd.DataFrame(souptable(table))
    mf_df.columns = ['','value']
    facts = pd.DataFrame.to_html(mf_df)

    mars_data["facts"] = facts



    #retrieve mars hemisphere enhanced photos
    hemi = requests.get("https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars")
    hsoup = bs(hemi.text, "html.parser")

    picsource = hsoup.find_all("div", class_="item")

    hemi_dicts = []
    baseurl = "https://astrogeology.usgs.gov"

    for i in range(len(picsource)):
        img_info = {}
        title = picsource[i]("h3")[0].text
        imagehunt = picsource[i].find("a").get("href", "")
        temp = requests.get(baseurl + imagehunt)
        tempsoup = bs(temp.text, "html.parser")
        image_ext = tempsoup.find("img", class_="wide-image").get("src","")
        img_url = baseurl + image_ext   
        img_info["title"] = title
        img_info["img_url"] = img_url
        hemi_dicts.append(img_info)

    mars_data["hemispheres"] = hemi_dicts

    #print(mars_data)

    return mars_data

#scrape()


