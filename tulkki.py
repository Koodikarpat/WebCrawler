from bs4 import BeautifulSoup
from urllib.parse import urlparse
from funktio import mysql_connector
import pymysql
import sys

url_domain = 'www.verkkokauppa.com'
url = 'https://www.verkkokauppa.com/fi/product/32458/dftrf/Seagate-Barracuda-2-TB-64-MB-7200-RPM-3-5-SATA-III-6-Gb-s-ko'
file_loc = 'master.html'
product_centre = {}
products = []
filterlvl1 = ['Komponentit', 'Tietokonekomponentit', 'Hiiret ja näppäimistöt',
              'Oheislaitteet' ,'Näytöt', 'PC Pelaaminen', 'Tietokonetarvikkeet',
              'N&auml;yt&ouml;t', 'Kiintolevyt, SSD ja verkkotallennus (NAS)']

def case_replace(input, case, productspecifier):
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
        'www.jimms.fi' : ['h1', 'class', 'name', 'span', 'itemprop', 'name', 'brand']
    },
    'productprices' : {
        'www.gigantti.fi' : ['div', 'class', 'product-price-container', 'span'],
        'www.verkkokauppa.com' : ['span', 'class', 'price-tag-price__euros', 'content'],
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
    filter2ext = {
    'Komponentit' : [
        ['Kotelo', 'Runko', 'Kotelot'],
        ['Prosessori', 'Prosessorit', 'Prosessori'],
        ['Kiintolevy' ,'Kiintolevyt / SSD-levyt', 'Sisäinen kiintolevy (SATA)', 'Sisäinen kiintolevy (SSD)', 'Kovalevyt'],
        ['Emolevy', 'Emolevyt', 'Emolevy'],
        ['Näytönohjain' ,'Näytönohjaimet', 'Näytönohjain'],
        ['Muisti', 'RAM-muisti', 'Muistit'],
        ['Virtalähde', 'Virtalähteet']
    ],
    'Oheislaitteet' : [
        ['Näyttö', 'Näytöt', 'Tietokoneen näyttö'],
        ['Hiiri', 'Hiiret'],
        ['Näppäimistö', 'Näppäimistöt'],
        ['Näppäimistö+Hiiri', 'Näppäimistöt ja hiiret', 'Näppäimistö ja hiiri'],
        ['Ulkoinen_kiintolevy']
    ]
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
    elif case in '2filter':
        if productspecifier in filter2ext:
            for object in filter2ext.get(productspecifier):
                if input in object:
                    return [object[0]]
            return ['NOT']
        return['NOT']
    else:
        return ['NOT']

def retvieve():
    global url_domain
    global url

    """
    file = open(file_loc, encoding='utf8')
    tulkki = BeautifulSoup(file, "html.parser")
    product_check(tulkki)
    """
    limit = 0
    querying = True
    try:
        connection = pymysql.connect(host='172.20.146.37', port=9696, database='crawltietokanta', user='inspect',
                                     password='cookies')
    except exception:
        sys.exit(exception)
    while querying:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM crawltietokanta.table_url LIMIT %(import)s, 10', {'import' : limit})
        for stuff in cursor:
            url_domain = urlparse(stuff[2]).hostname
            url = stuff[2]
            print(str(limit) + '. Checking...')
            url_domain = urlparse(stuff[2]).hostname
            tulkki = BeautifulSoup(stuff[1], "html.parser")
            product_check(tulkki)
        limit = limit + 10
        cursor.close()
    connection.close()

def product_check(tulkkaaja):
    global url_domain
    global url
    settings = case_replace(url_domain, 'stores', 'nope')
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
    settings = case_replace(url_domain, 'productfilter1', 'nope')
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
    settings = case_replace(url_domain, 'productfilter2', 'nope')
    if(settings[0] not in 'NOT'):
        if url_domain in 'www.jimms.fi':
            item = tulkkaaja.findAll(settings[1], {settings[2]: settings[3]}, {'itemprop': 'name'})[int(settings[0])].contents[1].contents[1].string
        else:
            item = tulkkaaja.find(settings[1], {settings[2], settings[3]}).contents[int(settings[0])].string
        prodstuff = case_replace(str(item), '2filter', product_centre['Tuoteluokka'])
        if prodstuff[0] not in 'NOT':
            product_centre['Osaluokka'] = prodstuff[0]
            product_specifier(tulkkaaja)
        else:
            print('Not a component what we would want: ' + url)

def product_specifier(tulkkaaja):
    global url_domain
    global url
    global product_centre
    settings = case_replace(url_domain, 'productnames', 'nope')
    settings2 = case_replace(url_domain, 'productprices', 'nope')
    if url_domain in 'www.gigantti.fi':
        itemname = tulkkaaja.find(settings[0], {settings[1]: settings[2]}).contents[0]
        itemprice = tulkkaaja.find(settings2[0], {settings2[1]: settings2[2]}).find(settings2[3]).contents[0]
    elif url_domain in 'www.verkkokauppa.com':
        itemname = tulkkaaja.find(settings[0], {settings[1]: settings[2]}).contents[0]
        itemprice = tulkkaaja.find(settings2[0], {settings2[1]: settings2[2]}).get('content')
    elif url_domain in 'www.systemastore.com':
        itemname = tulkkaaja.find(settings[0], {settings[1]: settings[2]}).find(settings[3], {settings[4]: settings[5]}).contents
        itemprice = tulkkaaja.find(settings2[0], {settings2[1]: settings2[2]}).find(settings2[3]).contents
    elif url_domain in 'www.jimms.fi':
        itembrand = tulkkaaja.find(settings[0], {settings[1]: settings[2]}).find(settings[3], {settings[4]: settings[6]}).contents
        itemname1 = tulkkaaja.find(settings[0], {settings[1]: settings[2]}).find(settings[3], {settings[4]: settings[5]}).contents
        itemname = itembrand[0] + ' ' + itemname1[0]
        itemprice = tulkkaaja.find(settings2[0], {settings2[1]: settings2[2]}).contents
        itemprice = itemprice[0]
    try:
        itemprice = itemprice.replace('\n', '')
        itemprice = itemprice.replace('r\n', '')
        itemprice = itemprice.replace('n', '')
        itemprice = itemprice.replace('\\', '')
    except:
        pass
    product_centre['Nimi'] = itemname
    product_centre['Hinta'] = itemprice
    product_centre['URL'] = url
    mysql_connector.tallennin(product_centre)
    product_centre = {}
    print('Product found!')

def main():
    retvieve()

main()