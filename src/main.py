import os
import sys
import re
import configparser
import requests
import json
import threading
import pdb

from requests.adapters import HTTPAdapter
from urllib3.util import Retry
from time import sleep
import datetime
from random import randint
from requests import RequestException
from bs4 import BeautifulSoup

from cli import ask


class PaperParser:
    def __init__(self, cookie, conf_list):
        self.cookie = {
            'PHPSESSID': cookie
        }
        self.conf_list = conf_list
        self.base = "https://dl.acm.org"
        self.session = requests.Session()

        self.filter_url = {
            'ISSCC': None,
            'MICRO': "conference/micro/proceedings",
            'ISCA': None,
            'DATE': None,
            'DAC': None,
            'ASP-DAC': None,
            'HPCA': None
        }

    def create_dir(self, path, name):
        os.chdir(path)
        try:
            os.mkdir(re.sub('[:/]', '', name))
        except:
            print('Directory exists.')
            pass

    def get_soup(self, url):
        r = self.requests_retry_session().get(url)
        r = requests.get(url, cookies=self.cookie)
        soup = BeautifulSoup(r.text, 'html.parser')
        return soup

    def requests_retry_session(
        self,
        retries=5,
        backoff_factor=0.3
    ):
        session = self.session or requests.Session()
        retry = Retry(
            total=retries,
            read=retries,
            connect=retries,
            backoff_factor=backoff_factor,
            status_forcelist=(500, 502, 504),
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session

    def get_conf_content(self):
        filtered_url = self.filter_url[self.conf_list]
        preceedings_url = f"{self.base}/{filtered_url}"

        soup = self.get_soup(preceedings_url)
        preceeding_list = soup.find_all('div', {'class': 'conference__title left-bordered-title'}) 
        breakpoint()

        preceeding = ask(type='list',
                        name='preceeding',
                        message='Select preceedings:',
                        choices=[
                            preceeding_list[num].find('a').text for num in range(len(preceeding_list))
                        ])['preceeding']
                
        for num in range(len(preceeding_list)):
            if preceeding_list[num].a.text.find(preceeding) == 0:
               preceeding_url = f"{self.base}{preceeding_list[num].a['href']}"
        self.create_dir(os.getcwd(), preceeding)

        soup = self.get_soup(preceeding_url)
        # content_wrapper = soup.find_all('div', {'class': 'table-of-content-wrapper'})[0].find_all('a')  
        content_wrapper = soup.find_all('div', {'class': 'table-of-content-wrapper'})[0].find_all('a')  

        headings = []
        for idx in range(len(content_wrapper)):
            try:
                if content_wrapper[idx]['id'].find('heading') == 0:
                    headings.append(content_wrapper[idx]['href'])
            except:
                pass
        
        workpath = os.getcwd()
        os.chdir(re.sub('[:/]', '', preceeding))
        for num_heading in range(len(headings)):
            heading_url = f"{self.base}{headings[num_heading]}"
            soup = self.get_soup(heading_url)
            pdfs = soup.find_all('h5', {'class': 'issue-item__title'})

            print("Downloading...")
            for num_pdf in range(len(pdfs)):
                pdf_url = pdfs[num_pdf].a['href']
                pdf_url = f'{self.base}{pdf_url}' 
                pdf_title = pdfs[num_pdf].text

                res = requests.get(pdf_url) 
                pdf = open(re.sub('[:/]', '', pdf_title) + ".pdf", 'wb')
                pdf.write(res.content)
                pdf.close()
            
    def start(self):
        self.get_conf_content()