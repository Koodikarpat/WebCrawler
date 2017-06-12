from asyncore import read

from bs4 import BeautifulSoup
import chardet

url = 'gigantti.fi'
fileloc = 'htmlaaa.txt'

def case_replace(input):
    stores = {
        'gigantti.fi' : ['li', 'class', 'tab specs active'],
        'verkkokauppa.com' : ['label', 'for', 'details-1'],
        'systemastore.com' : ['div', 'id', 'teknisettiedot'],
        'jimms.fi' : ['div', 'id', 'pinfo_propinfo']
    }

    if input in stores:
        return stores.get(input)
    else:
        return ['NOT']

def product_check(tulkkaaja, text):
    settings = case_replace(url)
    if(settings[0] != 'NOT'):
        if tulkkaaja.find(settings[0], { settings[1] : settings[2]}) is not None:
            print('Yes')
        else:
            print('No')


def tulkkikoulu(html):
    tulkki = BeautifulSoup(html, "html.parser")
    product_check(tulkki, html)


def main():
    lines = []
    try:
        file = open(fileloc)
    except:
        file = open(fileloc, encoding=chardet.detect(read(fileloc)).get('encoding'))

    for line in file:
        lines.append(line)

    for idea in lines:
        tulkkikoulu(idea)

main()