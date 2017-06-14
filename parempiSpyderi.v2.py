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

    def __init__(self, url, maxpages):
        self.urls = [url]
        self.maxpages = maxpages
        self.spider()

    def spider(self):
        htmltext = ""
        maara = 0
        #Otetaan seuraavassa luupissa ulos nykyiseltä urlilta kaikki html teksti
        while len(self.urls) > 0 and self.maxpages >= len(self.visited):
            try:
                htmltext = urllib.request.urlopen(self.urls[0]).read()
            except :
                pass
            #Nyt laitetaan se html parsinnan alaiseksi
            soup = BeautifulSoup(htmltext, "html.parser")
            url = self.urls[0]
            htmltextia = htmltext.decode("utf-8", "ignore")
            self.kirjuria(htmltextia, url)
            #tässä vaiheessa on tarkoitus kutsua uutta funktiota jossa otetaan SQL databaseen yhteys joka tallentaa
            #kaiken uuden tiedon muodossa (html, url, ID(jokaisella uniikki)
            print(url)

            print(len(self.urls))
            print("Visited: ", len(self.visited))
            testaus = bool(re.findall("https://www.jimms.fi" "|" "https://www.verkkokauppa.com" "|" "https://www.gigantti.fi", url))
            if maara <= 5:
                if testaus is False:
                    maara += 1
                else:
                    pass
            else:
                url = "https://www.verkkokauppa.com"
                maara = 0
            for tag in soup.findAll('a', href=True):
                tag['href'] = urllib.parse.urljoin(url, tag['href'])
                if tag['href'] not in self.visited:
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
    sivu = sys.argv[1]
    maxpages = int(sys.argv[2])
    x = paaosa(sivu, maxpages)

main()
