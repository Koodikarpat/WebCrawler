# -*- coding: utf-8 -*-
import re
import urllib.parse
import urllib.request
from bs4 import BeautifulSoup
import sys
import pymysql

class paaosa():
    urls = []
    visited = []
    def __init__(self):
        self.urls = ["https://www.jimms.fi/", "https://www.verkkokauppa.com/", "https://www.gigantti.fi/"]
        self.spider()

    def spider(self):
        while len(self.urls) > 0:
            url = self.urls[0]
            try:
                htmltext = urllib.request.urlopen(url).read()
                soup = BeautifulSoup(htmltext, "html.parser")
                htmltextia = htmltext.decode("utf-8", "ignore")
                self.kirjuria(htmltextia, url)
            except:
                pass

            print("Visited: ", len(self.visited))

            for tag in soup.findAll('a', href=True):
                tag['href'] = urllib.parse.urljoin(url, tag['href'])
                testaus = bool(re.findall("https://www.jimms.fi" "|" "https://www.verkkokauppa.com" "|" "https://www.gigantti.fi", tag['href']))
                if tag['href'] not in self.visited and testaus is True:
                    if tag['href'] not in self.urls and tag['href'] not in self.visited:
                        self.urls.append(tag['href'])

            self.visited.append(url)
            self.urls.pop(0)

    def kirjuria(self, html, url):

        soup = BeautifulSoup(html, "html.parser")
        for script in soup(['script', 'style']):
            script.extract()
        html = str(soup)
        conn = pymysql.connect(host='localhost', port='****', database='SpiderLair', user='****', password='*****', charset='utf8')
        cur = conn.cursor()
        kirjottaa = ("INSERT INTO hotomot"
                     "(html, url)"
                     "VALUES(%(hotoa)s, %(urli)s)")
        tuloo = {
            'hotoa': html,
            'urli': url,
        }
        try:
            cur.execute(kirjottaa, tuloo)
        except pymysql.err.InternalError:
            cur.close()
            conn.close()
            return(0)
        conn.commit()
        cur.close()
        conn.close()


def main():
   x = paaosa()

main()