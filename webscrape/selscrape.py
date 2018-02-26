import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

browser = webdriver.Chrome('/Users/adityanarkar/Downloads/chromedriver')
browser.get("https://play.google.com/store/apps/collection/topselling_free?hl=en")
time.sleep(1)

no_of_pagedowns = 20
body = browser.find_element_by_tag_name("body")
while no_of_pagedowns:
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(1)
    no_of_pagedowns-=1
product_link = ""
elements = browser.find_elements_by_class_name("details")
for element in elements:
        a_element = element.find_element_by_tag_name("a")
        # product_title = a_element.get_attribute("title")
        product_link = product_link + "\n" + a_element.get_attribute("href")
print product_link
browser.quit()

seperate_links = product_link.split("\n")
packageName = ""
for link in seperate_links:
    # packageName = packageName + link.split("=")[1] + "\n"
    packageName = packageName + link.split('=')[1]+'\n' if len(link.split("=")) > 1 else ""
print packageName

with open('packageNames.txt', 'w') as the_file:
    the_file.write(packageName)
# print element
