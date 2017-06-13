#!/usr/bin/env python
import sys
import pymysql

#yksin kertaisesti yhdistää databaseen
def luoja():
    conn = pymysql.connect(host='localhost', port=6969, database='MySQL', user='root', password='webcrawler' )
    cur = conn.cursor()
    #tehdään uusi table jonne lisätään pari saraketta (html, url, id)
    ror = "CREATE TABLE 'hotomoto' ("
    "id MEDIUMINT NOT NULL AUTO_INCREMENT,"
    "html TEXT,"
    "url TEXT,"
    "PRIMARY KEY (id) );"
    #tehdään lisäys kyseiseen tableen pääkoodissa jossa lisätään suoraan koodista tiedot eteenpäin
    #tallenetaan id teksti tiedostoon nimeltä id pääkoodissa ja kutsutaan sitä aina ennenkuin muokataan koodia
    #Tällöin saadaan uniikilla id:llä aina uusi html teksti toimimaan'
    cur.execute(ror)
    conn.commit()
    cur.close()
    conn.close()

def main():
    luoja()

main()