import urllib.parse
import urllib.request
from bs4 import BeautifulSoup
import sys
class paaosa():
    urls = []
    tuotteita = 0
    def spider(self, url, maxpages):
        self.urls = [url]
        visited = [url]
        htmltext = ""
        while len(self.urls) > 0 or maxpages == len(visited):
            try:
                htmltext = urllib.request.urlopen(self.urls[0]).read()
            except:
                print(self.urls[0])
            soup = BeautifulSoup(htmltext, "html.parser")
            url = self.urls[0]
            self.urls.pop(0)
            print(len(self.urls))

            for tag in soup.findAll('a', href=True):
                tag['href'] = urllib.parse.urljoin(url,tag['href'])
                if url in tag['href'] and tag['href'] not in visited:
                    self.urls.append(tag['href'])
                    visited.append(tag['href'])
            hinta = self.tutkija(url)

        print(visited)

    def tutkija(self, url):
        htmltext = urllib.request.urlopen(self.urls[0]).read()
        soup = BeautifulSoup(htmltext, "html.parser")
        hinta = soup.find('span', attrs={'itemprop':'price'}) or soup.find('span', attrs={'content':'price'})
        tuote = soup.find('span', attrs={'itemprop':'name'})
        if hinta != None:
            paragraphs = []
            for x in hinta:
                paragraphs.append(str(x))
            self.tuotteita += 1
            print(url)
            print(paragraphs)
            print(self.tuotteita)
        if tuote != None:
            lause = []
            for x in tuote:
                lause.append(str(x))
            print(lause)


def main():
    x = paaosa()
    sivu = sys.argv[1]
    maxpages = int(sys.argv[2])
    x.spider(sivu, maxpages)

main()