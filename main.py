'''
Author - Pasindu Sewmuthu
Date - 11 February 2022
Purpose - Python Web Scraper
'''

from bs4 import BeautifulSoup
import requests
import os
import shutil


def get_links():
    html = requests.get('https://coloringhome.com/categories').text
    soup = BeautifulSoup(html, 'lxml')

    header_list = []
    for header in soup.find_all('h2', {"class": "ctitle"}):
        header_list.append(header.string.replace('&amp;', '&'))

    link_list = {}
    for div in soup.find_all('div', {"class": "catts"}):
        attrs = soup.find_all('div', {"class": "catts"})
        for header in header_list:
            links = {}
            for a in attrs[header_list.index(header)].find("div", {"class": "catt catred"}).find("p").find("a"):
                links[f"https://coloringhome.com{a['href']}"] = a.string

            link_list[header] = links
