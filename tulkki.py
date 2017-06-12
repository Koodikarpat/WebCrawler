from bs4 import BeautifulSoup
spec_name = [ 'lisätiedot', 'tekniset tiedot', 'arvostelut', 'kuvaus', 'arvostelu' ]

def product_check(tulkkaaja, text):
    if tulkkaaja.find('li', { 'class' : 'tab specs active'}) is not None:
        print('Yes')
    else:
        print('No')


def tulkkikoulu(html):
    tulkki = BeautifulSoup(html, "html.parser")
    #tulkki.find("li", {"class": "tab specs active"})
    product_check(tulkki, html)


def main():
    lines = []
    with open('htmlaaa.txt') as filee:
        for line in filee:
            lines.append(line)
    for idea in lines:
        tulkkikoulu(idea)

main()