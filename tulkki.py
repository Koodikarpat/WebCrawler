from bs4 import BeautifulSoup
from urllib.parse import urlparse
import pymysql
import sys

url_domain = ''
url = ''
#fileloc = 'htmlaaa.txt'
product_centre = {}
products = []
filterlvl1 = ['Komponentit', 'Tietokonekomponentit', 'Hiiret ja näppäimistöt',
              'Oheislaitteet' ,'Näytöt', 'PC Pelaaminen', 'Tietokonetarvikkeet',
              'N&auml;yt&ouml;t', 'Kiintolevyt, SSD ja verkkotallennus (NAS)']
filterlvl2 = ['Runko', 'Prosessorit','Näytönohjaimet','Muistit','Emolevyt',
              'Kiintolevyt / SSD-levyt','Kovalevyt',
              'Emolevy','Näytönohjain','RAM-muisti','Sisäinen kiintolevy (SSD)',
              'Sisäinen kiintolevy (SATA)','Prosessori','Jäähdytin','Kotelot',
              'Jäähdytys','Hiiret','Näppäimistöt','Näytöt','Näppäimistöt ja hiiret',
              'Näppäimistö ja hiiri','Hiiri','Näppäimistö','Näyttö','Tietokoneen näyttö',
              'Virtalähde', 'Ulkoinen kiintolevy', '', '', '', '', '', '', '', '', '', '', '']

def case_replace(input, case):
    cases = {
    'stores' : {
        'www.gigantti.fi' : ['li', 'id', 'tab-specs'],
        'www.verkkokauppa.com' : ['label', 'for', 'details-1'],
        'www.systemastore.com' : ['div', 'id', 'teknisettiedot'],
        'www.jimms.fi' : ['div', 'id', 'pinfo_propinfo']
    },
    'productnames' : {
        'www.gigantti.fi' : ['h1', 'class', 'product-title'],
        'www.verkkokauppa.com' : ['h1', 'class', 'heading-page product__name-title'],
        'www.systemastore.com' : ['div', 'class', 'h1_title', 'span', 'itemprop', 'name'],
        'www.jimms.fi' : ['h1', 'class', 'name', 'span', 'itemprop', 'name']
    },
    'productprices' : {
        'www.gigantti.fi' : ['div', 'class', 'product-price-container', 'span'],
        'www.verkkokauppa.com' : ['div', 'class', 'price-tag-content__price-tag-price price-tag-content__price-tag-price--current', 'span', 'class', 'price-tag-price__euros'],
        'www.systemastore.com' : ['div', 'class', 'product_bar_specialpricetag', 'span'],
        'www.jimms.fi' : ['span', 'itemprop', 'price']

    },
    'productfilter1' : {
        'www.gigantti.fi' : ['3', 'ol', 'class', 'breadcrumbs S-1-1'],
        'www.verkkokauppa.com' : ['1', 'ul', 'class', 'breadcrumbs-container__breadcrumbs'],
        'www.systemastore.com' : ['3', 'div', 'class', 'nav_path'],
        'www.jimms.fi' : ['0', 'li', 'itemprop', 'itemListElement']
    },
    'productfilter2' : {
        'www.gigantti.fi' : ['0', 'td', 'class', 'any-3-4 S-1-2'],
        'www.verkkokauppa.com' : ['2', 'ul', 'class', 'breadcrumbs-container__breadcrumbs'],
        'www.systemastore.com' : ['5', 'div', 'class', 'nav_path'],
        'www.jimms.fi' : ['2', 'li', 'itemprop', 'itemListElement']
    }
    }
    if case in cases:

        if input in cases.get('stores'):
            if case is 'stores':
                return cases.get('stores').get(input)
            elif case is 'productnames':
                return cases.get('productnames').get(input)
            elif case is 'productprices':
                return cases.get('productprices').get(input)
            elif case is 'productfilter1':
                return cases.get('productfilter1').get(input)
            elif case is 'productfilter2':
                return cases.get('productfilter2').get(input)
        else:
            return ['NOT']
    else:
        return ['NOT']


def retvieve():
    global url_domain
    global url
    integer = 0
    limit = 0
    try:
        connection = pymysql.connect(host='172.20.146.37', port=9696, database='crawltietokanta', user='inspect',
                                     password='cookies')
    except exception:
        sys.exit(exception)
    while integer <= 10:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM crawltietokanta.table_url LIMIT %(import)s, 100', {'import' : limit})
        for stuff in cursor:
            url_domain = urlparse(stuff[2]).hostname
            url = stuff[2]
            print(str(integer) + '. Checking...')
            url_domain = urlparse(stuff[2]).hostname
            tulkki = BeautifulSoup(stuff[1], "html.parser")
            product_check(tulkki)
        integer = integer + 1
        limit = limit + 100
        print(limit)
        cursor.close()
    connection.close()

def product_check(tulkkaaja):
    global url_domain
    global url
    settings = case_replace(url_domain, 'stores')
    if(settings[0] != 'NOT'):
        if tulkkaaja.find(settings[0], { settings[1] : settings[2]}) is not None:
            product_identifier(tulkkaaja)
        else:
            print('Not a product: ' + url)
    else:
        print('Domain incorrect: ' + url_domain)


def product_identifier(tulkkaaja):
    global url_domain
    global url
    components = [filterlvl1[0], filterlvl1[1], filterlvl1[6], filterlvl1[8]]
    settings = case_replace(url_domain, 'productfilter1')
    if url_domain in 'www.jimms.fi':
        stuff = tulkkaaja.findAll(settings[1], {settings[2]: settings[3]}, {'itemprop' : 'name'})
        speficclass = stuff[1].contents[1].contents[1].string
    else:
        stuff = tulkkaaja.find(settings[1], {settings[2]: settings[3]}).contents
        speficclass = stuff[int(float(settings[0]))].string
    if speficclass in filterlvl1:
        if speficclass not in components:
            speficclass = filterlvl1[3]
        else:
            speficclass = filterlvl1[0]
        product_centre['Tuoteluokka'] = str(speficclass)
        product_class_specifier(tulkkaaja)
    else:
        print('Not a component: ' + url)

def product_class_specifier(tulkkaaja):
    global url_domain
    global url
    settings = case_replace(url_domain, 'productfilter2')
    if(settings[0] not in 'NOT'):
        if url_domain in 'www.jimms.fi':
            item = tulkkaaja.findAll(settings[1], {settings[2]: settings[3]}, {'itemprop': 'name'})[int(settings[0])].contents[1].contents[1].string
        else:
            item = tulkkaaja.find(settings[1], {settings[2], settings[3]}).contents[int(settings[0])].string
        if(item in filterlvl2):
            if item not in (filterlvl2[26]):
                if item in (filterlvl2[0]):
                    item = 'Kotelo'
                product_centre['Osaluokka'] = str(item)
            else:
                product_centre['Tuoteluokka'] = 'Oheislaitteet'
                product_centre['Osaluokka'] = str(item)
            product_specifier(tulkkaaja)
        else:
            print('Not a component what we would want: ' + url)


def product_specifier(tulkkaaja):
    global url_domain
    global url
    global product_centre
    settings = case_replace(url_domain, 'productnames')
    settings2 = case_replace(url_domain, 'productprices')
    if url_domain in 'www.gigantti.fi':
        itemname = tulkkaaja.find(settings[0], {settings[1]: settings[2]}).contents
        itemprice = tulkkaaja.find(settings2[0], {settings2[1]: settings2[2]}).find(settings2[3]).contents
    elif url_domain in 'www.verkkokauppa.com':
        itemname = tulkkaaja.find(settings[0], {settings[1]: settings[2]}).contents
        itemprice = tulkkaaja.find(settings2[0], {settings2[1]: settings2[2]}).find(settings2[3], {settings2[4]: settings2[5]}).contents
    elif url_domain in 'www.systemastore.com':
        itemname = tulkkaaja.find(settings[0], {settings[1]: settings[2]}).find(settings[3], {settings[4]: settings[5]}).contents
        itemprice = tulkkaaja.find(settings2[0], {settings2[1]: settings2[2]}).find(settings2[3]).contents
    elif url_domain in 'www.jimms.fi':
        itemname = tulkkaaja.find(settings[0], {settings[1]: settings[2]}).find(settings[3], {settings[4]: settings[5]}).contents
        itemprice = tulkkaaja.find(settings2[0], {settings2[1]: settings2[2]}).contents
    try:
        itemprice = str(itemprice).replace(r'\n', '').replace('n', '').replace('\\', '')
    except:
        pass
    print(str(itemname))
    product_centre['Nimi'] = itemname
    product_centre['Hinta'] = itemprice
    product_centre['URL'] = url
    if product_centre not in products:
        products.append(product_centre)
        product_centre = {}
        print('Product found!')

def main():
    retvieve()

    if len(products) is 0:
        print('No products here!')
    else:
        for product in products:
            print(product)

main()