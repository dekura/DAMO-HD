'''
@Author: Guojin Chen
@Date: 2020-03-28 09:42:08
@LastEditTime: 2020-03-28 11:28:12
@Contact: cgjhaha@qq.com
@Description: EPE DB class
'''

'''
@Author: Guojin Chen
@Date: 2019-11-15 13:29:39
@LastEditTime: 2019-11-26 20:07:13
@Contact: cgjhaha@qq.com
@Description: database for epe nums
'''
import sqlite3
import numpy as np

class EPE_DB:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.c = self.conn.cursor()
        # self.c.execute('''DROP TABLE IF EXISTS EPE
        # ''')
        self.c.execute('''CREATE TABLE IF NOT EXISTS EPE
        (ID INTEGER PRIMARY KEY AUTOINCREMENT  NOT NULL,
        NAME           TEXT     NOT NULL,
        EPE_NUM         INT     NOT NULL,
        TYPE           TEXT     NOT NULL,
        GDSX           REAL     NOT NULL,
        GDSY           REAL     NOT NULL
        );''')

        self.c.execute('''CREATE TABLE IF NOT EXISTS PVB
        (ID INTEGER PRIMARY KEY AUTOINCREMENT  NOT NULL,
        NAME           TEXT     NOT NULL,
        PVB_NUM        REAL     NOT NULL,
        TYPE           TEXT     NOT NULL
        );''')
        self.c.execute('''CREATE TABLE IF NOT EXISTS MEPE
        (ID INTEGER PRIMARY KEY AUTOINCREMENT  NOT NULL,
        NAME           TEXT     NOT NULL,
        HOW_MANY        INT     NOT NULL,
        ABS_MEPE        INT     NOT NULL,
        ZERO_PER       REAL     NOT NULL
        );''')

        print('new database {}'.format(db_path))
        print('connect to table successfuly')
        self.conn.commit()

    def insert_one(self, NAME, EPE_NUM, TYPE, GDSX, GDSY):
        c = self.c
        # print "INSERT INTO EPE (NAME,EPE_NUM,TYPE,GDSX,GDSY) VALUES ('{}', {}, '{}', {}, {});".format(NAME, EPE_NUM, TYPE, GDSX, GDSY)
        c.execute("INSERT INTO EPE (NAME,EPE_NUM,TYPE,GDSX,GDSY) VALUES ('{}', {}, '{}', {}, {});".format(NAME, EPE_NUM, TYPE, GDSX, GDSY))
        self.conn.commit()

    def insert_one_pvb(self, NAME, PVB_NUM, TYPE):
        c = self.c
        # print "INSERT INTO EPE (NAME,EPE_NUM,TYPE,GDSX,GDSY) VALUES ('{}', {}, '{}', {}, {});".format(NAME, EPE_NUM, TYPE, GDSX, GDSY)
        c.execute("INSERT INTO PVB (NAME,PVB_NUM,TYPE) VALUES ('{}', {}, '{}');".format(NAME, PVB_NUM, TYPE))
        self.conn.commit()

    def get_all_name(self):
        c = self.c
        cursor = c.execute("SELECT NAME FROM EPE")
        names = set()
        for row in cursor:
            names.add(row[0])
        return names

    def get_names_mepeless(self, epe_bar):
        c = self.c
        cursor = c.execute("SELECT NAME FROM MEPE WHERE ABS_MEPE<{}".format(epe_bar))
        names = set()
        for row in cursor:
            names.add(row[0])
        return names

    def get_epes_byname(self, name):
        c = self.c
        cursor = c.execute("SELECT EPE_NUM FROM EPE WHERE NAME='{}'".format(name))
        epe_nums = []
        for row in cursor:
            epe_nums.append(row[0])
        return epe_nums

    def insert_one_mepe(self, name, how_many, abs_mepe, zero_per):
        c = self.c
        mepe_id = c.execute("SELECT ID FROM MEPE WHERE NAME='{}'".format(name))
        id = mepe_id.fetchone()
        if id:
            c.execute("INSERT OR REPLACE INTO MEPE (ID, NAME,HOW_MANY,ABS_MEPE,ZERO_PER) VALUES ('{}', '{}', {}, '{}', {});".format(id[0], name, how_many, abs_mepe, zero_per))
        else:
            c.execute("INSERT INTO MEPE (NAME,HOW_MANY,ABS_MEPE,ZERO_PER) VALUES ('{}', {}, '{}', {});".format(name, how_many, abs_mepe, zero_per))
        self.conn.commit()

    def parse_mepe(self):
        print('parsing mepe...')
        names = self.get_all_name()
        for name in list(names):
            epes = self.get_epes_byname(name)
            epes = np.array(epes)
            how_many = len(epes)
            abs_mepe = np.nanmean(np.abs(epes))
            zero_per = len(np.where(epes == 0)[0])/how_many
            self.insert_one_mepe(name, how_many, abs_mepe, zero_per)

    def close(self):
        self.conn.close


if __name__ == '__main__':
    db_path = '/Users/dekura/Downloads/ovia5.db'
    epedb = EPE_DB(db_path)

    epedb.close()



