from bs4 import BeautifulSoup
spec_name = [ 'lisätiedot', 'tekniset tiedot', 'arvostelut', 'kuvaus', 'arvostelu' ]

def product_check():
    hei = '';

def tulkkikoulu(html):
    div = []
    tulkki = BeautifulSoup(html, "html.parser")
    for stiff in tulkki.findAll('div'):
        div.append(stiff)
        print(stiff)


def main():
    lines = []
    with open('htmlaaa.txt') as filee:
        for line in filee:
            lines.append(line)
    tulkkikoulu(lines[0])

main()