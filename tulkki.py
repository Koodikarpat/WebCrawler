from bs4 import BeautifulSoup
import pymysql

product_details = ''
url = 'verkkokauppa.com'
fileloc = 'master.html'
products = []
filterlvl1 = ['Komponentit', 'Tietokonekomponentit', 'Hiiret ja näppäimistöt', 'Oheislaitteet' ,'Näytöt', 'PC Pelaaminen', 'N&auml;yt&ouml;t']
filterlvl2 = []

def case_replace(input, case):
    cases = {
    'stores' : {
        'gigantti.fi' : ['li', 'id', 'tab-specs'],
        'verkkokauppa.com' : ['label', 'for', 'details-1'],
        'systemastore.com' : ['div', 'id', 'teknisettiedot'],
        'jimms.fi' : ['div', 'id', 'pinfo_propinfo']
    },
    'productnames' : {
        'gigantti.fi' : ['h1', 'class', 'product-title'],
        'verkkokauppa.com' : ['h1', 'class', 'heading-page product__name-title'],
        'systemastore.com' : ['div', 'class', 'h1_title', 'span', 'itemprop', 'name'],
        'jimms.fi' : ['h1', 'class', 'name', 'span', 'itemprop', 'name']
    },
    'productprices' : {
        'gigantti.fi' : ['div', 'class', 'product-price-container', 'span'],
        'verkkokauppa.com' : ['div', 'class', 'price-tag-content__price-tag-price price-tag-content__price-tag-price--current', 'span', 'class', 'price-tag-price__euros'],
        'systemastore.com' : ['div', 'class', 'product_bar_specialpricetag', 'span'],
        'jimms.fi' : ['span', 'itemprop', 'price']

    },
    'productfilter' : {
        'gigantti.fi' : ['3', 'ol', 'class', 'breadcrumbs S-1-1'],
        'verkkokauppa.com' : ['1', 'ul', 'class', 'breadcrumbs-container__breadcrumbs'],
        'systemastore.com' : ['2', 'div', 'class', 'navpath'],
        'jimms.fi' : ['2', 'ol', 'class', 'breadcrumb']
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
            elif case is 'productfilter':
                return cases.get('productfilter').get(input)
        else:
            return ['NOT']
    else:
        return ['NOT']


def product_identifier(tulkkaaja):
    global product_details
    settings = case_replace(url, 'productfilter')
    stuff = list(tulkkaaja.find(settings[1], {settings[2] : settings[3]}))
    speficclass = stuff[int(float(settings[0]))].string.strip('\n')
    print(speficclass)
    if speficclass in filterlvl1:
        if speficclass is not filterlvl1[0] or speficclass is not filterlvl1[0]:
            speficclass = filterlvl1[3]
            product_details = speficclass + ' : '
            product_specifier(tulkkaaja)

def product_specifier(tulkkaaja):
    global product_details
    settings = case_replace(url, 'productnames')
    if len(settings) is 3:
        itemname = tulkkaaja.find(settings[0], {settings[1]: settings[2]}).contents
    elif len(settings) is 4:
        itemname = tulkkaaja.find(settings[0], {settings[1]: settings[2]}).find(settings[3]).contents
    elif len(settings) is 5:
        itemname = tulkkaaja.find(settings[1], {settings[2]: settings[3]}).find(settings[4]).contents
    elif len(settings) is 6:
        itemname = tulkkaaja.find(settings[0], {settings[1]: settings[2]}).find(settings[3], {settings[4]: settings[5]}).contents

    settings = case_replace(url, 'productprices')
    if len(settings) is 3:
        itemprice = tulkkaaja.find(settings[0], {settings[1]: settings[2]}).contents
    elif len(settings) is 4:
        itemprice = tulkkaaja.find(settings[0], {settings[1]: settings[2]}).find(settings[3]).contents
    elif len(settings) is 5:
        itemprice = tulkkaaja.find(settings[1], {settings[2]: settings[3]}).find(settings[4]).contents
    elif len(settings) is 6:
        itemprice = tulkkaaja.find(settings[0], {settings[1]: settings[2]}).find(settings[3], {settings[4]: settings[5]}).contents

    if product_details + itemname[0] + ' : ' + itemprice[0] not in products:
        product_details = product_details + itemname[0].strip('\n') + ' : ' + itemprice[0].strip('\n')
        products.append(product_details)

def product_check(tulkkaaja):
    settings = case_replace(url, 'stores')
    if(settings[0] != 'NOT'):
        if tulkkaaja.find(settings[0], { settings[1] : settings[2]}) is not None:
            product_identifier(tulkkaaja)


def main():
    lines = []
    try:
        file = open(fileloc, encoding='utf-8')
    except:
        print('idc')

#    for line in file:
#        lines.append(line)
#
#    for idea in lines:
#        tulkki = BeautifulSoup(idea, "html.parser")
#        product_check(tulkki)
    tulkki = BeautifulSoup(file, "html.parser")
    product_check(tulkki)
    for shit in products:
        print(shit)
main()