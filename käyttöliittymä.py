from funktio import mysql_connector


class Tuote(object):
    def __init__(self, nimi, hinta, url):
        self.nimi = nimi
        self.hinta = hinta
        self.url = url


filter2ext = {
    'komponentit': [
        'kotelo',
        'intel_prosessori',
        'amd_prosessori',
        'kiintolevy',
        'emolevy',
        'näytönohjain',
        'muisti',
        'virtalähde'
    ],
    'oheislaitteet': [
        'näyttö',
        'hiiri',
        'näppäimistö',
        'näppäimistö+hiiri',
    ]
}

def class_specifier(text):
    if text in 'komponentit' or text in 'oheislaitteet':
        return False
    else:
        return True

def class_component_specifier(_class, text):
    if text in filter2ext.get(_class):
        return False
    else:
        return True

def retviever(query):
    tuotteita = []
    products = mysql_connector.noutaja(preference1 + '_' + preference2)
    for product in products:
        tuote = Tuote(product[0], product[1], product[2])
        tuotteita.append(tuote)
        return tuotteita


def main():
    while True:
        preference1 = input('Haluatko komponentteja vai oheislaitteita? (komponentit, oheislaitteet)').lower()
        if class_specifier(preference1):
            print('Väärä syöte!')
        else:
            break
    while True:
        for stuff in filter2ext.get(preference1):
            print(stuff)
        preference2 = input('Valitse jokin yllämainituista!').lower()
        if class_component_specifier(preference1, preference2):
            print('Väärä syöte!')
        else:
            break
    print('Haetaan osia...')
    tuote_array = retviever(preference1 + '_' + preference2)
    while True:
        if len(tuote_array) >= 10:
            preference3 = input('Tuotteita on suuri määrä, haluatko järjestellä ne hinnan mukaan? (yes tai no)').lower()
            if preference3 in 'yes':
                tuote_array = sorted(tuote_array, key=lambda product: product.hinta)
                break
            elif preference3 in 'no':
                break
            else:
                print('Väärä syöte!')
        else:
            break

    for stuff in tuote_array:
        print('Nimi: ' + stuff.nimi + '             Hinta: ' + str(stuff.hinta) + '\nURL: ' + stuff.url + '\n\n')

if __name__ == '__main__':
    main()