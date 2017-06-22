import pymysql

class mysql_connector:

    def tallennin(x):
        productclass = x.get('Tuoteluokka').lower()
        underclass = x.get('Osaluokka').lower()
        productname = x.get('Nimi')
        productprice = x.get('Hinta')
        producturl = x.get('URL')

        if underclass in 'prosessori':
            processorproducer = str(productname.partition(' ')[0]).lower()

        conn = pymysql.connect(host='172.20.146.37', port=9696, database='crawltietokanta', user='inspect', password='cookies')
        cur = conn.cursor()

        if underclass in "prosessori":
            tablename = productclass + '_' + processorproducer + '_' + underclass
            print(tablename)
            s = "CREATE TABLE IF NOT EXISTS " + tablename + "(id INT auto_increment, nimi LONGTEXT, hinta FLOAT, url LONGTEXT, PRIMARY KEY (id));"\
            "INSERT INTO " + tablename + "(nimi, hinta, url) VALUES ( '" + productname + "', " + productprice + ", '" + producturl + "');"

            cur.execute(s)
            conn.commit()

        else:
            tablename = productclass + '_' + underclass
            print(tablename)
            s = "CREATE TABLE IF NOT EXISTS " + tablename + "(id INT auto_increment, nimi LONGTEXT, hinta FLOAT, url LONGTEXT, PRIMARY KEY (id));"\
            "INSERT INTO " + tablename + "(nimi, hinta, url) VALUES ( '" + productname + "', " + str(productprice) + ", '" + producturl + "');"
            cur.execute(s)
            conn.commit()

        cur.close()
        conn.close()
