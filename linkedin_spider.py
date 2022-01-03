from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from parsel import Selector
import parameters
import csv

SLEEP_TIME_SHORT = 1
SLEEP_TIME_LONG = 2

writer = csv.writer(open(parameters.result_file, 'w'))
writer.writerow(['name', 'job_title', 'school', 'ln_url'])

driver = webdriver.Chrome('C:\chromedriver.exe')
driver.get('https://www.linkedin.com/')
sleep(SLEEP_TIME_SHORT)

# Log into Linkedin
login_button = driver.find_element_by_xpath('/html/body/nav/div/a[2]')
login_button.click()
sleep(SLEEP_TIME_SHORT)
username_input = driver.find_element_by_xpath('//*[@id="username"]')
username_input.send_keys(parameters.username)
password_input = driver.find_element_by_xpath('//*[@id="password"]')
password_input.send_keys(parameters.password)
login_button = driver.find_element_by_xpath('//*[@id="organic-div"]/form/div[3]/button')
login_button.click()
sleep(SLEEP_TIME_SHORT)

# Go to Google search and get urls
driver.get('https://www.google.com/')
sleep(SLEEP_TIME_SHORT)
search_input = driver.find_element_by_xpath('//input[contains(@title, "Search")]')
search_input.send_keys(parameters.search_query)
search_input.send_keys(Keys.ENTER)
sleep(SLEEP_TIME_SHORT)
profiles = driver.find_elements_by_xpath('//div[@class="g"]/div/div/div/a')
urls = [profile.get_attribute('href') for profile in profiles]

# Get into each profile and parse
for url in urls:
    try:
        driver.get(url)
        sleep(SLEEP_TIME_LONG)
        sel = Selector(text=driver.page_source)
        name = sel.xpath('//title/text()').extract_first().split(' | ')[0]
        job_title = sel.xpath('//div[contains(@class, "text-body-medium break-words")]/text()').extract_first().strip()
        schools = sel.xpath('//h3[contains(@class, "school-name")]/text()').extract()
        ln_url = driver.current_url
        writer.writerow([name, job_title, schools, ln_url])

        # Don't want to actually send the connection request when I test
        # driver.find_element_by_xpath('//*[text()="Connect"').click()
        # driver.find_element_by_xpath('//*[text()="Send now"').click()

    except:
        pass

driver.quit()







