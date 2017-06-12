import urllib.parse
import urllib.request
from bs4 import BeautifulSoup
import sys


class paaosa():
    urls = []
    visited = []

    def __init__(self, url, maxpages):
        self.urls = [url]
        self.maxpages = maxpages
        self.spider()

    def spider(self):
        htmltext = ""
        #Otetaan seuraavassa luupissa ulos nykyiseltä urlilta kaikki html teksti
        while len(self.urls) > 0 and self.maxpages >= len(self.visited):
            try:
                htmltext = urllib.request.urlopen(self.urls[0]).read()
            except :
                pass
            #Nyt laitetaan se html parsinnan alaiseksi
            soup = BeautifulSoup(htmltext, "html.parser")
            c = open("htmlaaa.txt", "a")
            c.write("%s\n" % soup)
            c.close()
            #tässä vaiheessa on tarkoitus kutsua uutta funktiota jossa otetaan SQL databaseen yhteys joka tallentaa
            #kaiken uuden tiedon muodossa (html, url, ID(jokaisella uniikki)
            url = self.urls[0]
            print(url)

            print(len(self.urls))
            print("Visited: ", len(self.visited))
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

def main():
    c = open("htmlaaa.txt", "w")
    sivu = sys.argv[1]
    maxpages = int(sys.argv[2])
    x = paaosa(sivu, maxpages)

main()