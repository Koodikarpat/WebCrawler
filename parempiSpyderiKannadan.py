import urllib.parse
import urllib.request
from bs4 import BeautifulSoup
import sys


class paaosa():
    urls = []
    tuotteita = 0
    visited = []
    loppuloop = 0
    seuraavasivu = ["https://www.jimms.fi/fi", "https://www.gigantti.fi"]
    maxpages = 100

    def __init__(self, url, maxpages):
        self.urls = [url]
        self.maxpages = maxpages
        self.spider()

    def spider(self):
        htmltext = ""
        while len(self.urls) > 0 and self.maxpages >= len(self.visited):
            try:
                htmltext = urllib.request.urlopen(self.urls[0]).read()
            except:
                pass
            c = open("htmlaaa.txt", "a")
            c.write("%s\n" % htmltext)
            c.close()

            soup = BeautifulSoup(htmltext, "html.parser")
            url = self.urls[0]
            print(url)

            print(len(self.urls))
            print("Visited: ", len(self.visited))
            for tag in soup.findAll('a', href=True):
                tag['href'] = urllib.parse.urljoin(url, tag['href'])
                if tag['href'] not in self.visited:
                    if tag['href'] not in self.urls and tag['href'] not in self.visited:
                        self.urls.append(tag['href'])
                        tag['oma'] = str(tag['href'])
                        a = tag['oma'].encode("ascii", "ignore")
                        x = open("visit.txt", "a")
                        x.write("%s\n" % a)
                        x.close()
            self.visited.append(url)
            hinta = self.tutkija(url)
            self.urls.pop(0)

    def tutkija(self, url):
        try:
            htmltext = urllib.request.urlopen(self.urls[0]).read()
            soup = BeautifulSoup(htmltext, "html.parser")
            hinta = soup.find("div", attrs={"class": "product-price-container"}) or soup.find('span', attrs={'itemprop': 'price'})
            tuote = soup.find("h1", attrs={"class":"heading-page product__name-title"})\
                    or soup.find('h1', attrs={'class': 'product-title'})\
                    or soup.find("span", attrs={"itemprop": "name"})

            if hinta != None:
                paragraphs = []
                for x in hinta:
                    paragraphs.append(str(x))
                self.tuotteita += 1
                print(url)
                print("Tuotteen hinta:", paragraphs)
                print("Löydettyjä hintoja:", self.tuotteita)
            if tuote != None:
                lause = []
                for x in tuote:
                    lause.append(str(x))
                print("Tuotteen nimi: ", lause)

        except (urllib.error.HTTPError, urllib.error.URLError, ValueError):
            return (0)
        except UnicodeEncodeError:
            return(0)

def main():
    x = open("visit.txt", "w")
    c = open("htmlaaa.txt", "w")
    x.close()
    sivu = sys.argv[1]
    maxpages = int(sys.argv[2])
    x = paaosa(sivu, maxpages)


main()