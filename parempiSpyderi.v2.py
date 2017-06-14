# -*- coding: utf-8 -*-
#python 3.5.2

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
        htmltext = ""
        #Otetaan seuraavassa luupissa ulos nykyiseltä urlilta kaikki html teksti
        while len(self.urls) > 0:
            url = self.urls[0]
            try:
                htmltext = urllib.request.urlopen(url).read()
                self.kirjuria(htmltextia, url)
            except:
                pass
            #Nyt laitetaan se html parsinnan alaiseksi
            soup = BeautifulSoup(htmltext, "html.parser")
            htmltextia = htmltext.decode("utf-8", "ignore")
            #tässä vaiheessa on tarkoitus kutsua uutta funktiota jossa otetaan SQL databaseen yhteys joka tallentaa
            #kaiken uuden tiedon muodossa (html, url, ID(jokaisella uniikki)
            print(url)

            print(len(self.urls))
            print("Visited: ", len(self.visited))

            for tag in soup.findAll('a', href=True):
                tag['href'] = urllib.parse.urljoin(url, tag['href'])
                testaus = bool(re.findall("https://www.jimms.fi" "|" "https://www.verkkokauppa.com" "|" "https://www.gigantti.fi", tag['href']))
                if tag['href'] not in self.visited and testaus is True:
                    if tag['href'] not in self.urls and tag['href'] not in self.visited:
                        self.urls.append(tag['href'])
                        #Tämä koodi parsii kaikki linkit html koodista ja laittaa ne urls listalle
                        #Tästä listasta otamme seuraavalla kerralla aina uuden urlin ja käymme sen läpi
                        #tämä toistuu kunnes netti sivu on käyty täysin läpi


            self.visited.append(url)
            self.urls.pop(0)

    def kirjuria(self, html, url):
        #kirjoittaa html tekstin sekä urlin tietokantaan
        htmltext = html
        urli = url

        soup = BeautifulSoup(html, "html.parser")
        for script in soup(['script', 'style']):
            script.extract()
        html = str(soup)

        conn = pymysql.connect(host='localhost', port=6969, database='SpiderLair', user='root', password='webcrawler', charset='utf8')
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
