#!/usr/bin/env python
import sys
from __future__ import print_function
import pymysql

#yksin kertaisesti yhdistää databaseen
def luoja(sql):
    conn = pymysql.connect(host='localhost', port=6969, user='root', passwd='webcrawler', db='MySql')
    cur = conn.cursor()
    #tehdään uusi table jonne lisätään pari saraketta (html, url, id)
    nimi = sql
    CREATE TABLE nimi (
      id MEDIUMINT NOT NULL AUTO_INCREMENT,
      html CHAR()
    );
    #tehdään lisäys kyseiseen tableen pääkoodissa jossa lisätään suoraan koodista tiedot eteenpäin
    #tallenetaan id teksti tiedostoon nimeltä id pääkoodissa ja kutsutaan sitä aina ennenkuin muokataan koodia
    #Tällöin saadaan uniikilla id:llä aina uusi html teksti toimimaan'

    cur.execute(ssss)

    conn.commit()
    cur.close()
    conn.close()

def main():
    eka = sys.argv[1]
    luoja(eka)

main()