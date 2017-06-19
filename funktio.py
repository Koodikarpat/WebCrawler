import pymysql

def tallennin(x):
    conn = pymysql.connect(host='localhost', port=6969, database='SpiderLair', user='root', password='webcrawler',
                           charset='utf8')
    cur = conn.cursor()

    if x[2] == "Prosessori":
        s = ("INSERT INTO (%s), (x[3]"
             "()"
             "VALUES(%(tuottaja)s,");
        d = {
            "tuottaja": x[3],
        }

        cur.execute(s,d)

        e = ("INSERT INTO (%s), (x[4]"
            "(hinta, url)"
            "VALUES(%(hinta)s, %(url)s");

        f = {
            " hinta": x[5],
            " url ": x[6],
        }

        cur.execute(e,f)
        #puuttuu tarkistin onko tuotetta.
    else:
        stmt = "SHOW TABLES LIKE (%s), (x[2]) "
        cursor.execute(stmt)
        result = cursor.fetchone()

        if result:
            s = ("INSERT INTO (%s), (x[2])"
            "(hinta, url)"
            "VALUES(%(hinta)s, %(url)s");
        d = {
        " hinta" : x[3],
        " url " : x[4],
        }
        cur.execute(s,d)
        else:
            s = """ CREATE TABLE IF NOT EXISTS (%s), (x[2]) (
                                        id integer PRIMARY KEY,
                                        hinta VARCHAR(10),
                                        url LONG TEXT,
                                    ); """;
            cur.execute(s);

            a = ("INSERT INTO (%s), (x[2]"
                 "(hinta, url)"
                 "VALUES(%(hinta)s, %(url)s");

            d = {
                " hinta": x[3],
                " url ": x[4],
            }
                cur.execute(a,d)

        conn.commit()
        cur.close()
        conn.close()