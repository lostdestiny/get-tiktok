from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import re
import urllib.request as geturl
import os
import sys
import getopt


error = 0


def get_webpage(url, cachedId='', basePath='D:/'):
    # Loads webpage using firefox browser and returns the entire page as soup
    driver = webdriver.Firefox()
    driver.get(url)
    # Wait until all video links are loaded
    page = driver.find_element_by_tag_name('body')
    time.sleep(2)
    i = 0
    while i < 10:
        page.send_keys(Keys.PAGE_DOWN)
        i += 1
    # More efficient way instead of sleep but does not work
    # element = WebDriverWait(driver, 10).until(element_has_css_class(
    # (By.ID, 'video-feed-item'), "video-feed-item"))
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    driver.quit()
    fileName = basePath + 'cached' + str(cachedId) + '.html'
    with open(fileName, 'w+', encoding='utf-8') as file:
        file.write(str(soup))
    print('Created file with name cached' + str(cachedId) + '.html')
    return soup


# No key input with 2 s delay only
def get_webpage_fast(url, cachedId='', basePath='D:/'):
    # Loads webpage using firefox browser and returns the entire page as soup
    driver = webdriver.Firefox()
    driver.get(url)
    # More efficient way instead of sleep but does not work
    # element = WebDriverWait(driver, 10).until(element_has_css_class(
    # (By.ID, 'video-feed-item'), "video-feed-item"))
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()
    fileName = basePath + 'cached' + str(cachedId) + '.html'
    with open(fileName, 'w+', encoding='utf-8') as file:
        file.write(str(soup))
    print('Created file with name cached' + str(cachedId) + '.html')
    return soup


def get_urls_from_user_tiktok(soup):
    listOfUrl = []
    for items in soup.find_all("a", class_="video-feed-item-wrapper"):
        # Search for links pointing to single-video page in  the attributes
        getAttr = re.search('(?:href=")[^"]*', str(items))
        # .group() is the method to get all the string from match object
        # Substitutes with an empty string
        vidUrl = re.sub('(href=")', '', getAttr.group())
        listOfUrl.append(vidUrl)
    return listOfUrl


# There are two CSS filters identied as of date
def find_links_from_filter(soup):
    foundList = []
    if soup.find_all("div", class_="video-card-browse") != []:
        foundList = soup.find_all("div", class_="video-card-browse")

    elif soup.find_all("div", class_="video-card") != []:
        foundList = soup.find_all("div", class_="video-card")

    return foundList


# Sometimes loaded website dont contain the tag
# Thus try finding video-feed-item-wrapper first
def get_src_from_video_page(soup):
    srcUrl = ''
    foundLinks = find_links_from_filter(soup)
    if foundLinks != []:
        for items in foundLinks:
            srcAttr = re.search('(?:src=")[^"]*', str(items))
            checkForImage = re.search('(?:https://p)', srcAttr.group())
            if checkForImage:
                print('Skipping found images...')
            else:
                if srcAttr:
                    srcUrl = re.sub('(src=")', '', srcAttr.group())
                    print('Extracted src:\n{} \n'.format(srcUrl))
                else:
                    print('srcAttr does not exist')
    else:
        print('No video links found')

    return srcUrl

    #
    # if soup.find_all("div", class_="video-card-browse") != []:
    #     for items in soup.find_all("div", class_="video-card-browse"):
    #         srcAttr = re.search('(?:src=")[^"]*', str(items))
    #         checkForImage = re.search('(?:https://p)', srcAttr.group())
    #         if checkForImage:
    #             print('Skipping found images...')
    #         else:
    #             if srcAttr:
    #                 srcUrl = re.sub('(src=")', '', srcAttr.group())
    #                 print('Extracted src:\n{} \n'.format(srcUrl))
    #             else:
    #                 print('srcAttr does not exist')
    #
    # elif soup.find_all("div", class_="video-card") != []:
    #     for items in soup.find_all("div", class_="video-card"):
    #         srcAttr = re.search('(?:src=")[^"]*', str(items))
    #         # Videos comes from https://v...
    #         checkForImage = re.search('(?:https://p)', srcAttr.group())
    #         if checkForImage:
    #             print('Skipping found images...')
    #         else:
    #             if srcAttr:
    #                 srcUrl = re.sub('(src=")', '', srcAttr.group())
    #                 print('Extracted src:\n{} \n'.format(srcUrl))
    #             else:
    #                 print('srcAttr does not exist')


def check_user_existence(url):
    driver = webdriver.Firefox()
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()
    soupMainBody = soup.find_all("div", class_="main-body")
    if soupMainBody != []:
        for items in soupMainBody:
            found = items.find("div", class_="avatar")
            if found:
                print('{} found'.format(url))
                return 1
        print('No user avatar found. Stopping program...'.format(userHandle))
        global error
        error += 1
        return 0
    else:
        error += 1
        print('User {} not found. Stopping program...'.format(userHandle))
        return 0


# The video list page is named cached.html
def get_soup_from_live_page(url, path='D:/caches'):
    return get_webpage(url, '', path)


def get_soup_from_cached_page(url, path='D:/'):
    fileName = path + 'cached' + '.html'
    soup = BeautifulSoup(features="html.parser")
    try:
        fp = open(fileName, 'r', encoding='utf-8')
        soup = BeautifulSoup(fp, 'html.parser')
        print('Obtaining links from cached page')
    except FileNotFoundError:
        print('Obtaining links from live page...')
        soup = get_soup_from_live_page(url, path)

    return soup


def main():
    # Pass first argument
    global error
    try:
        userHandle = sys.argv[1]
    except IndexError:
        print('Please input the Tiktok users name(without @)')
        error += 1

    urlBase = "https://www.tiktok.com/@"
    urlUser = urlBase + userHandle

    # Check if path is in the right format argument
    # path = re.match('[A-Za-z][:][/]', sys.argv[1])

    if check_user_existence(urlUser):
        1

    if error > 0:
        print('Too many errors. Stopping program')
        return 0

    path = 'D:/Tiktok/@'
    try:
        path = path + userHandle + '/'
        os.mkdir(path)
        print('Saving to {}'.format(path))
    except FileExistsError:
        # do something when dir already exists
        print('{} exists'.format(path))

    # Try to get list of videoss from a cached user page
    soup = get_soup_from_cached_page(urlUser, path)
    listUrl = get_urls_from_user_tiktok(soup)
    print('NO OF LINKS FOUND:{}'.format(len(listUrl)))

    # Get last videos

    # convert return type of enumerator to list
    for idx, url in reversed(list(enumerate(listUrl))):
        # Get soup from a page and get the src of the video
        soupNow = get_webpage_fast(url, idx, path)
        src = get_src_from_video_page(soupNow)
        print('Downloading from url...')
        # Download videos from the video site
        fileName = path + 'video{}.mp4'.format(idx)
        if src != '':
            geturl.urlretrieve(src, fileName)
        else:
            print('Link extraction failed')

    # If single video pagesare already cached use this function instead
    # for i in range(4):
    #     soup = get_soup_from_cached_page(i)
    #     src = get_src_from_video_page(soup)
    #     if src != '':
    #         geturl.urlretrieve(src, 'video{}.mp4'.format(i))
    #     else:
    #         print('Link extraction failed')


if __name__ == '__main__':
    main()


"""

# Extract only interesting items
#shopItems = webpage.find('div', id="containerShop").findAll('span')

    # Search for 'href="' and the following string after it,
    # recursively (denoted by *) and continue to match
    # when you dont find " (denoted by '^"' : compliment of double aphostrophe)
    #vidUrl = re.search('href="[^"]*', str(items))

# Same as above but uses the parenthesis
getAttr = re.search('(?:href=")[^"]*', str(items))
"""
