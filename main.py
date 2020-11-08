from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import time
import re
from selenium.common.exceptions import InvalidArgumentException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import NoSuchWindowException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException
import sqlite3
from time import gmtime, strftime
from random import random

email = "rimescald@mail.ru"
password = "Qxh8SYNqe3nwASr"

hipsters_file = "data/groups/hipster_groups.txt"
ordinary_file = "data/groups/ordinary_groups.txt"

# Configure web driver
opts = Options()
# opts.headless = True
# assert opts.headless
browser = Firefox(options=opts)

# Create database
conn = sqlite3.connect("data/fb_profiles/fb_people" + ".sqlite")
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS profiles
                  (fb_id text primary key, posts text, hipster text, timestamp text)
               """)
conn.commit()

# Entrance point
page_link = "https://facebook.com"
browser.get(page_link)
inputElement = browser.find_element_by_id("email")
inputElement.send_keys(email)
inputElement = browser.find_element_by_id("pass")
inputElement.send_keys(password)
inputElement = browser.find_element_by_id("u_0_b")
time.sleep(1)
inputElement.click()
time.sleep(1)

# with open(hipsters_file) as file_in:
#     hipster_groups = []
#     for line in file_in:
#         hipster_groups.append(line)
#
# users = []
# for group in hipster_groups:
#     try:
#         # Collect hipster links
#         browser.get(group)
#         for i in range(0, 100):
#             browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#             time.sleep(2*random())
#         html_source = browser.page_source
#         web_page = BeautifulSoup(html_source, 'html.parser')
#         text = ""
#         reviews = web_page.find_all(class_='oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl oo9gr5id gpro0wi8 lrazzd5p')
#         for review in reviews:
#             if review.has_attr('href'):
#                 hipster = review['href']
#                 hipster = hipster.split("?")[0]
#                 users.append(hipster)
#
#     except(TimeoutException, ElementNotInteractableException,
#            NoSuchElementException, WebDriverException, NoSuchWindowException):
#         print("We've got a selenium exception here")
#
# hipster = 1
# for users_link in users:
#     try:
#         browser.get(users_link)
#         for i in range(0, 10):
#             browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#             time.sleep(2*random())
#         html_source = browser.page_source
#         web_page = BeautifulSoup(html_source, 'html.parser')
#         text = ""
#         posts = web_page.find_all(class_='kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x c1et5uql')
#         for post in posts:
#             text = text + "\n" + post.getText()
#         if len(text) > 0:
#             timestamp = strftime("%Y-%m-%d %H:%M:%S", gmtime())
#             app_data = [users_link, text, hipster, timestamp]
#             cursor.execute("INSERT OR IGNORE INTO profiles VALUES (?,?,?,?)", app_data)
#             conn.commit()
#             app_data_return = []
#
#     except(TimeoutException, ElementNotInteractableException,
#            NoSuchElementException, WebDriverException, NoSuchWindowException):
#         print("We've got a selenium exception here")
#

## Ordinary
hipster = 0
users = []
with open(ordinary_file) as file_in:
    ordinary_groups = []
    for line in file_in:
        ordinary_groups.append(line)

for group in ordinary_groups:
    try:
        # Collect hipster links
        browser.get(group)
        for i in range(0, 100):
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2*random())
        html_source = browser.page_source
        web_page = BeautifulSoup(html_source, 'html.parser')
        text = ""
        reviews = web_page.find_all(class_='oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl oo9gr5id gpro0wi8 lrazzd5p')
        for review in reviews:
            if review.has_attr('href'):
                hipster = review['href']
                hipster = hipster.split("?")[0]
                users.append(hipster)

    except(TimeoutException, ElementNotInteractableException,
           NoSuchElementException, WebDriverException, NoSuchWindowException):
        print("We've got a selenium exception here")


for user_link in users:
    try:
        browser.get(user_link)
        for i in range(0, 10):
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2*random())
        html_source = browser.page_source
        web_page = BeautifulSoup(html_source, 'html.parser')
        text = ""
        posts = web_page.find_all(class_='kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x c1et5uql')
        for post in posts:
            text = text + "\n" + post.getText()
        if len(text) > 0:
            timestamp = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            app_data = [user_link, text, hipster, timestamp]
            cursor.execute("INSERT OR IGNORE INTO profiles VALUES (?,?,?,?)", app_data)
            conn.commit()
            app_data_return = []

    except(TimeoutException, ElementNotInteractableException,
           NoSuchElementException, WebDriverException, NoSuchWindowException):
        print("We've got a selenium exception here")