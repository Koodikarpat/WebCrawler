import pymysql

dictionary = {'Tuoteluokka': 'Komponentit', 'Osaluokka': 'Emolevy', 'Nimi': 'MSI Z270 GAMING PRO CARBON, ATX -emolevy + Phanteks 400mm RGB LED -valonauha', 'Hinta': '199,00', 'URL': 'https://www.jimms.fi/fi/Product/Show/131798/z270-gaming-pro-carbon-plb/msi-z270-gaming-pro-carbon-atx-emolevy-phanteks-400mm-rgb-led-valonauha'}

def tallennin(x):
	productclass = x.get('Tuoteluokka')
	underclass = x.get('Osaluokka').lower()
	productname = x.get('Nimi')
	productprice = x.get('Hinta')
	producturl = x.get('URL')
	
	if underclass in 'Osaluokka':
		processorproducer = str(productname.partition(' ')[0]).lower()
		
	conn = pymysql.connect(host='172.20.146.37', port=9696, database='crawltietokanta', user='inspect', password='cookies')
	cur = conn.cursor()

	if underclass == "Prosessori":
		tablename = processorproducer + ' ' + underclass
		s = "CREATE TABLE IF NOT EXISTS 'crawltietokanta'.'%(tablename)s' ('ID' INT NOT NULL AUTO_INCREMENT, 'Nimi' LONGTEXT NULL, 'Hinta' LONGTEXT NULL, 'URL' LONGTEXT NULL, PRIMARY KEY ('ID') ENGINE = InnoDB DEFAULT CHARACTER SET = utf8"
		d = { "tablename": tablename }

		cur.execute(s,d)

		e = ("INSERT INTO 'crawltietokanta'.'%(tablename)s' (Nimi, Hinta, URL) VALUES(%(nimi)s, %(hinta)s, %(url)s");

		f = {
			"tablename" : tablename,
			"nimi": productname,
            "hinta": productprice,
            "url": producturl
        }

		cur.execute(e,f)
		conn.commit()
		cur.close()
		conn.close()
		
	else:
		tablename = underclass
		stmt = "SHOW TABLES LIKE (%(tablename)s)"
		stmta = {
			"tablename": tablename
		}
		cur.execute(stmt, stmta)
		result = cur.fetchone()

		if result:
			s = "INSERT INTO 'crawltietokanta'.'%(tablename)s' (Nimi, Hinta, URL) VALUES(%(nimi)s, %(hinta)s, %(url)s)"
			d = {
			"tablename" : tablename,
			"nimi" : productname,
			"hinta" : productprice,
			"url" : producturl
			}
			cur.execute(s,d)
		else:
			s = "CREATE TABLE IF NOT EXISTS 'crawltietokanta'.'%(tablename)s' ('ID' INT NOT NULL AUTO_INCREMENT, 'Nimi' LONGTEXT NULL, 'Hinta' LONGTEXT NULL, 'URL' LONGTEXT NULL, PRIMARY KEY ('ID') ENGINE = InnoDB DEFAULT CHARACTER SET = utf8"
			f = {
			'tablename' : tablename
			}
			cur.execute(s, f);

			a = ("INSERT INTO 'crawltietokanta'.'%(tablename)s' (Nimi, Hinta, URL) VALUES(%(nimi)s, %(hinta)s, %(url)s");

			d = {
				"nimi" : productname,
                "hinta": productprice,
                "url ": producturl
            }
			cur.execute(a,d)

		conn.commit()
		cur.close()
		conn.close()
	print('Done')
		
tallennin(dictionary)