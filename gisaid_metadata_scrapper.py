from seleniumwire import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from datetime import datetime
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as cond
from selenium.common.exceptions import NoAlertPresentException, MoveTargetOutOfBoundsException, TimeoutException, ElementClickInterceptedException
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.action_chains import ActionChains
import tqdm
import glob
import os
import sys
import logging
import json

FORMAT = '%(asctime)s:%(levelname)s:%(message)s'

logging.basicConfig(filename='GISAID_Download_Log.log', level=logging.DEBUG,
    format=FORMAT)

class GisaidCoVMetadataScrapper:
    def __init__(self, headless: bool = False):
        options = webdriver.ChromeOptions() 
        prefs = {}
        path = os.getcwd()
        prefs["profile.default_content_settings.popups"] = 0
        prefs["download.default_directory"] = path
        options.add_experimental_option("prefs", prefs)
        options.headless = headless
        logging.info('Attempting to establish Chrome session')
        print('Attempting to establish Chrome session')
        self.driver = webdriver.Chrome(chrome_options=options)
        logging.info('Established Chrome session')
        print('Established Chrome session')
        self.driver.implicitly_wait(1000)
        logging.info('Waiting to stabilize Chrome session')
        print('Waiting to stabilize Chrome session')
        self.driver.set_window_size(1366, 2000)
        logging.info('Setting Chrome window size')
        print('Setting Chrome window size')

    def remove_sys_curtain(self):
        logging.info('Removing sys curtain')
        try:
            self.driver.execute_script("document.getElementById('sys_curtain').remove()")
            logging.info('Successfully removed sys curtain')
        except:
            logging.info('No sys curtain to remove')
            pass

    def login(self, username: str, password: str):
        logging.info('Loading login page')
        print('Loading login page')
        self.driver.get("https://platform.gisaid.org/epi3/frontend")
        time.sleep(10)
        logging.info('Successfully loaded login page')
        print('Successfully loaded login page')
        login = self.driver.find_element_by_name("login")
        logging.info('Found username input field')
        print('Found username input field')
        login.send_keys(username)

        passwd = self.driver.find_element_by_name("password")
        logging.info('Found password input field')
        print('Found password input field')
        passwd.send_keys(password)

        login_box = self.driver.find_element_by_class_name("form_button_submit")
        logging.info('Found login form box')
        print('Found login form box')

        self.remove_sys_curtain()

        logging.info('Attempting to submit login credentials')
        print('Attempting to submit login credentials')
        self.driver.execute_script("document.getElementsByClassName('form_button_submit')[0].click()")
        logging.info('Clicked login credentials submissin button')
        print('Clicked login credentials submissin button')
        logging.info('Waiting for login credentials to load')
        print('Waiting for login credentials to load')
        WebDriverWait(self.driver, 60).until(cond.staleness_of(login_box))
        logging.info('Sucessfully logged in.')

    def load_epicov(self):
        time.sleep(2)
        self._go_to_seq_browser()
        print('Filtering Samples')
        filtering = ['Whole Genomes only selected', 'High Coverage Selected', 'Low coverage excluded']
        time.sleep(8)
        parent_form = self.driver.find_elements_by_class_name(
            "sys-form-fi-cb")
        for index,i in enumerate(parent_form):
            inp = i.find_element_by_tag_name("input")
            inp.click()
            print(filtering[index])
            time.sleep(5)
        samples_count = int(self.driver.find_elements_by_xpath("//*[contains(text(), 'Total:')]")[0].text.split(" ")[1].replace(",", ""))
        parent_form = self.driver.find_element_by_id("yui-dt0-th-c-liner")
        inp = parent_form.find_element_by_tag_name("input")
        inp.click()
        print('Total Samples Selected:', samples_count)
        time.sleep(8)

        self.go_to_next_page()
        print('Capturing metadata request')
        time.sleep(5)
        gisaid_request = self.driver.last_request
        print(gisaid_request)
        url = str(gisaid_request)
        temp = url.split("27")
        new_url = temp[0] + str(0) + temp[1] + str(samples_count) + temp[2]
        print(new_url)
        get_request = requests.get(new_url, timeout = 120)
        json.dump(get_request.json(), open("metadata.json", "w"), indent = 6)
        # awk 'NR>2 {print $0}' metadata.json | head -n -7 | sed '$s/\,//g' | sed 's/"records"://g' > formatted.json
        print("Metadata Saved!!!")
        time.sleep(2)
        self.driver.close()
            

    def _go_to_seq_browser(self):
        self.remove_sys_curtain()
        self.driver.find_element_by_link_text("EpiCoV™").click()
        print('Clicked on EpiCov')

        time.sleep(10)

        self.remove_sys_curtain()
        self.driver.find_elements_by_xpath("//*[contains(text(), 'Browse')]")[0].click()
        print('Clicked on Browse')

    def go_to_next_page(self):
        try:
            self.driver.find_element_by_xpath("//*[contains(text(), 'next >')]").click()
        except ElementClickInterceptedException:
            self.driver.execute_script("document.getElementById('sys_curtain').remove()")
            self.driver.find_element_by_xpath("//*[contains(text(), 'next >')]").click()
