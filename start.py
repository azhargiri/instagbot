from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys as Key
import time
import random
import os
import configparser



class instagram(object):
    url = 'https://www.instagram.com'
    username = ""
    login_url = url + '/accounts/login'
    password = ""
    
urlCollectionFilename = 'url_collection.txt'
credentFile = 'credent.txt'

config = configparser.ConfigParser()
config.read(credentFile)

instagram.username=config['default']['username']
instagram.password=config['default']['password']

if None in (instagram.username, instagram.password):
    print('Please configure username and password')
    exit(400)

likeListSelector='a.zV_Nj'
likerSelector='div.Igw0E.rBNOH.eGOV_.ybXk5._4EzTm.XfCBB.HVWg4._0mzm-.ZUqME'
# likeSelector='div.Igw0E.rBNOH.eGOV_.ybXk5._4EzTm.XfCBB.HVWg4._0mzm-.ZUqME'
likerButtonSelector='button[type=button]._0mzm-.sqdOP.L3NKy'

# read urlCollection from file
with open(urlCollectionFilename) as f:
    urlCollection = [line.strip() for line in f]

# Create a new instance of the Firefox driver
driverOptions = webdriver.FirefoxOptions()
# driverOptions.add_experimental_option('prefs', {'intl.accept_languages': 'en, en_US'})
# driver = webdriver.Firefox(firefox_options = driverOptions)

driver = webdriver.Firefox(firefox_options = driverOptions)

# go to the google home page
driver.get(instagram.login_url)

driver.implicitly_wait(10)

# find the element that's name attribute is q (the google search box)
inputUsernameLogin = driver.find_element_by_css_selector('input[name=username]')
inputPasswordLogin = driver.find_element_by_css_selector('input[name=password]')
submitLoginButton = driver.find_element_by_css_selector('button[type=submit]')

inputUsernameLogin.send_keys(instagram.username)
inputPasswordLogin.send_keys(instagram.password)

driver.implicitly_wait(2)

submitLoginButton.click()

driver.implicitly_wait(10)
time.sleep(10)

# WebDriverWait(driver, 20).until(
#         EC.presence_of_element_located((By.TAG_NAME, 'body'))
#         )

while(True):
    for url in urlCollection:
        driver.get(url)
        WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.TAG_NAME, 'body'))
                )

        likeListButton= driver.find_element_by_css_selector(likeListSelector)
        likeListButton.click()

        WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role=dialog].pbNvD.fPMEg'))
                )

        likerDialog = driver.find_element_by_css_selector('div[role=dialog].pbNvD.fPMEg')
        likerDialog.click()

        _likerDialog = driver.find_element_by_css_selector('div.Igw0E.IwRSH.eGOV_.vwCYk.i0EQd > div')
        _likerDialog.send_keys(Key.TAB)
        time.sleep(1)
        _likerDialog.send_keys(Key.TAB)
        time.sleep(1)
        _likerDialog.send_keys(Key.TAB)
        time.sleep(1)

        nScroll = 0;
        maxNScroll = 10;
        while(nScroll < maxNScroll):
            _likerDialog.send_keys(Key.ARROW_DOWN)
            time.sleep(1)
            nScroll += 1



        likerList = likerDialog.find_elements_by_css_selector(likerSelector)
        print(likerList)
        
        max_liker_count = 3
        n = 0
        
        peopleToLike = []

        while n < max_liker_count:
            liker = likerList[n]
            followButton = liker.find_element_by_css_selector(likerButtonSelector)
            accountToFollow = liker.find_element_by_css_selector('a')

            if followButton.text == 'Follow' or followButton.text == 'Ikuti':
                peopleToLike.append(accountToFollow.text)

                # discard
                # followButton.click()
                # print('Following %s' % (accountToFollow.text))
                # url = 'https://www.instagram.com/' + accountToFollow.text

                # driver.get(url)
                # driver.implicitly_wait(5)
                # follow = driver.find_element_by_css_selector('button')
                # follow[0].click()



                # peopleFollowButton = driver.find_elements_by_css_selector('button')[0]

                # if peopleFollowButton.text == 'Ikuti' or peopleFollowButton.text == 'Follow':
                #     peopleFollowButton.click()
                # else:
                #     print('This people %s is already followed', accountToFollow.text)

                # time.sleep(3)
            else:
                print('Already following this user %s (link: %s)' % (accountToFollow.text, accountToFollow.text))
                driver.implicitly_wait(2)
                max_liker_count = max_liker_count + 1

            n = n + 1 
            print('------')

        print(peopleToLike)

        n = 0
        nTry = 0
        maxNTry = 20
        while(n < max_liker_count or nTry < maxNTry): 
            people = peopleToLike[n]

            driver.get('https://www.instagram.com/%s' % ( people ))
            time.sleep(3)
            follow = driver.find_element_by_css_selector('button')[0]

            if follow.text == 'Follow' or follow.text == 'Ikuti':
                follow.click()
                n += 1

            nTry += 1
            time.sleep(5)



    time.sleep(random.randrange(60, 120, 10))
