import time

import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By


def get_parent_from_div_by_text(driver, text):
    try:
        return driver.find_element(By.XPATH, "//div[contains(text(), '" + text + "')]") \
            .find_element(By.XPATH, "..").text
    except AttributeError as err:
        return 'ERROR'


def get_x_parent_from_span_by_text(driver, text, x):
    try:
        element = driver.find_element(By.XPATH, "//span[contains(text(), '" + text + "')]")
        for c in range(x):
            element = element.find_element(By.XPATH, "..")
        return element.text
    except AttributeError as err:
        return 'ERROR'

def get_x_parent_button_from_span_by_text(driver, text, x):
    try:
        element = driver.find_element(By.XPATH, "//span[contains(text(), '" + text + "')]")
        for c in range(x):
            element = element.find_element(By.XPATH, "..")
        return element
    except AttributeError as err:
        return 'ERROR'


class BeerSpider(scrapy.Spider):
    name = 'beer-spider'

    def start_requests(self):
        url = "https://www.brewerydb.com/brewknowledge"
        yield SeleniumRequest(url=url, callback=self.parse)

    def parse(self, response):
        driver = response.request.meta["driver"]
        # scroll to the end of the page 10 times
        for x in range(0, 10):
            # scroll down by 10000 pixels
            ActionChains(driver).scroll_by_amount(0, 10000).perform()

        # waiting 2 seconds for the products to load

        subpageUrls = []
        for i in  range(156):
            time.sleep(5)
            for article in driver.find_elements(By.XPATH, "//article"):
                url = article.find_element(By.XPATH, "..").get_attribute("href")
                subpageUrls.append(url)
                print('Added URL:', url)

            button=get_x_parent_button_from_span_by_text(driver,"Next",1)
            button.click()



        for index in range(0, 300):
            url = subpageUrls[index]
            yield SeleniumRequest(url=url, callback=self.parse_detailpage)
            time.sleep(1)
        # beer_name = article.find_element(By.CSS_SELECTOR,".brew-card__title").text
        # company = article.find_element(By.CSS_SELECTOR,".brew-card__subtitle").text

        # beer= {
        #    'url':url,
        #    'beer_name':beer_name,
        #    'company':company
        # }

    def parse_detailpage(self, response):
        driver = response.request.meta["driver"]
        time.sleep(1)
        url = driver.current_url
        abv = get_parent_from_div_by_text(driver, 'ABV')
        brew_style = get_x_parent_from_span_by_text(driver, 'Brew Style', 3)
        primary_flavor_notes = get_x_parent_from_span_by_text(driver, 'Primary Flavor Notes', 1)
        srm = get_parent_from_div_by_text(driver, 'SRM')
        ibu = get_x_parent_from_span_by_text(driver, 'IBU', 2)
        serving_temperature = get_x_parent_from_span_by_text(driver, 'Serving Temperature', 2)

        yield {
            'url': url,
            'abv': abv,
            'brew_style': brew_style,
            "primary_flavor_notes": primary_flavor_notes,
            "srm": srm,
            "ibu": ibu,
            "serving_temperature": serving_temperature
        }
