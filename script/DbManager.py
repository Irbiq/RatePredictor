import pymysql
import datetime
from collections import defaultdict

class DbManager:
    def __init__(self, host='localhost', port=3306, user='root', password='1234', db='banks', charset='utf8'):
        self.__host = host
        self.__port = port
        self.__user = user
        self.__password = password
        self.__db = db
        self.__charset = charset
        self.__conn = pymysql.connect(host=self.__host, port=self.__port, user=self.__user, password=self.__password,
                                      db=self.__db, charset=self.__charset)

    def get_connection_new(self):
        return pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.password, db=self.db,
                               charset=self.charset)

    @property
    def conn(self):
        return self.__conn

    def select_all(self):
        bank_rate_time = defaultdict(dict)
        cur = self.__conn.cursor()
        cur.execute("SELECT * FROM bank")
        for row in cur:
            bank_name = row[1]
            usd_exch = row[2]
            time = row[3]
            bank_rate_time[bank_name][time] = usd_exch
        cur.close()
        return bank_rate_time

    def select_all_nb(self):
        rate_time = {}
        cur = self.__conn.cursor()
        cur.execute("SELECT * FROM nac_bank")
        for row in cur:
            usd_exch = row[1]
            time = row[2]
            rate_time[time] = usd_exch
        cur.close()
        return rate_time

    def insert_exchs(self, exch_list):
        cur = self.__conn.cursor()
        insert_cur = ("INSERT INTO bank"
                      "(bank,usd,time)"
                      "VALUES (%s, %s,%s)")
        for data in exch_list:
            st = (data.bank, data.usd, datetime.datetime.now())
            cur.execute(insert_cur, st)
        cur.close()
        self.__conn.commit()

    def insert_exchs_nb(self, exch_list):
        cur = self.__conn.cursor()
        insert_cur = ("INSERT INTO nac_bank"
                      "(usd,time)"
                      "VALUES (%s,%s)")
        for data in exch_list:
            st = (data.usd, datetime.datetime.now())
            cur.execute(insert_cur, st)
        cur.close()
        self.__conn.commit()

    def insert_exchs_nb_single(self, exch):
        cur = self.__conn.cursor()
        insert_cur = ("INSERT INTO nac_bank"
                      "(usd,time)"
                      "VALUES (%s,%s)")
        st = (exch, datetime.datetime.now())
        cur.execute(insert_cur, st)
        cur.close()
        self.__conn.commit()