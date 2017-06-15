from bs4 import BeautifulSoup

product_details = ''
url = 'gigantti.fi'
fileloc = 'htmlaaa.txt'
products = []
filterlvl1 = ['Komponentit', 'Tietokonekomponentit', 'Hiiret ja näppäimistöt', 'Oheislaitteet' ,'Näytöt', 'PC Pelaaminen', 'Tietokonetarvikkeet', 'N&auml;yt&ouml;t']
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
        'systemastore.com' : ['3', 'div', 'class', 'nav_path'],
        'jimms.fi' : ['0', 'li', 'itemprop', 'itemListElement']
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
    components = [filterlvl1[0], filterlvl1[1], filterlvl1[6]]
    global product_details
    settings = case_replace(url, 'productfilter')
    if url in 'jimms.fi':
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

        product_details = speficclass + ' : '
        product_specifier(tulkkaaja)


def product_specifier(tulkkaaja):
    global product_details
    settings = case_replace(url, 'productnames')
    settings2 = case_replace(url, 'productprices')
    if url in 'gigantti.fi':
        itemname = tulkkaaja.find(settings[0], {settings[1]: settings[2]}).contents
        itemprice = tulkkaaja.find(settings2[0], {settings2[1]: settings2[2]}).find(settings2[3]).contents
    elif url in 'verkkokauppa.com':
        itemname = tulkkaaja.find(settings[0], {settings[1]: settings[2]}).contents
        itemprice = tulkkaaja.find(settings2[0], {settings2[1]: settings2[2]}).find(settings2[3], {settings2[4]: settings2[5]}).contents
    elif url in 'systemastore.com':
        itemname = tulkkaaja.find(settings[0], {settings[1]: settings[2]}).find(settings[3], {settings[4]: settings[5]}).contents
        itemprice = tulkkaaja.find(settings2[0], {settings2[1]: settings2[2]}).find(settings2[3]).contents
    elif url in 'jimms.fi':
        itemname = tulkkaaja.find(settings[0], {settings[1]: settings[2]}).find(settings[3], {settings[4]: settings[5]}).contents
        itemprice = tulkkaaja.find(settings2[0], {settings2[1]: settings2[2]}).contents
    product_details = product_details + itemname[0].strip('\n') + ' : ' + itemprice[0].strip('\n')
    if product_details not in products:
        product_details
        products.append(product_details)

def product_check(tulkkaaja):
    settings = case_replace(url, 'stores')
    if(settings[0] != 'NOT'):
        if tulkkaaja.find(settings[0], { settings[1] : settings[2]}) is not None:
            product_identifier(tulkkaaja)


def main():
    lines = []
    file = open(fileloc, encoding='utf-8')

    for line in file:
        lines.append(line)

    for idea in lines:
        tulkki = BeautifulSoup(idea, "html.parser")
        product_check(tulkki)

    for product in products:
        print(product)

main()