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
    try:
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
                for a in attrs[header_list.index(header)].find("div").find("p").find("a"):
                    links[f"https://coloringhome.com{a['href']}"] = a.string

                link_list[header] = links

        return link_list
    except:
        return "Error"


def greb_images():
    link_list = get_links()

    try:
        if link_list != "Error":
            for header, links in link_list.items():
                os.makedirs(f"img/{header}", exist_ok=True)
                for link, name in links.items():
                    print(f"Fetching from {link}")
                    os.makedirs(f"img/{header}/{name}", exist_ok=True)

                    html = requests.get(link).text
                    soup = BeautifulSoup(html, 'lxml')
                    images = soup.find_all(
                        'div', {"class": "thumbnail side-corner-tag"})

                    i = 1
                    for img in images:
                        url = f"https://coloringhome.com{img['src']}"

                        try:
                            ext = url[url.rindex('.'):]
                            if ext.startswith('.png'):
                                ext = '.png'
                            elif ext.startswith('.jpg'):
                                ext = '.jpg'
                            elif ext.startswith('.jfif'):
                                ext = '.jfif'
                            elif ext.startswith('.com'):
                                ext = '.jpg'
                            elif ext.startswith('.svg'):
                                ext = '.svg'

                            if len(str(i)) == 1:
                                i = f"00{i}"
                            elif len(str(i)) == 2:
                                i = f"0{i}"

                            data = requests.get(url, stream=True)
                            filename = f"{name}.{str(i)}{ext}"

                            with open(f"img/{header}/{name}/{filename}", 'wb') as file:
                                shutil.copyfileobj(data.raw, file)

                            i += 1
                        except:
                            pass
        else:
            return "Error"
    except:
        return "Error"
