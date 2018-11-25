import os
import sys
import sqlite3 as sq3
from datetime import datetime

class ToDoDate:

    def __init__(self, dbname):
        '''

        SQLite會自動維護一個系統表單「sqlite_master」，
        裡面會有我們創建的表單信息。

        '''
        self.conn = sq3.connect(dbname)
        cur = self.conn.execute('SELECT * FROM sqlite_master')
        name_rows = cur.fetchall()
        self.tablist =list()
        if name_rows:
            func = lambda x : x != 'sqlite_sequence'
            for r in filter(func, [row[1] for row in name_rows]):
                self.tablist.append(r)
            for dex, tab in enumerate(self.tablist):
                print(f'{dex}. {tab}')
        else:
            print('尚未建立清單！')
    

    def sql_create(self, name=None):
        
        self.conn.execute(
            f'''CREATE TABLE {name} (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                CONTENT TEXT,
                DATE TEXT,
                STATUS TEXT
            )''' )
        

    def sql_alter(self, oldname, newname):
        self.conn.execute(
            f'''ALTER TABLE {oldname}
            RENAME TO {newname}'''
        )
    
    def sel_deltab(self, tab):
        self.conn.execute(f'DROP TABLE {tab}')

    def sql_insert(self, item):
        dt = datetime.now()
        nowdate = dt.strftime('%F')
        self.conn.execute(
            f'''INSERT INTO {self.sql_create()} (CONTENT, DATE, STATUS)
            VALUES ('{item}', {nowdate}, 0)''')

    
    def sql_update(self, cent, sta, num):
        self.conn.execute(
            f'''UPDATE {self.sql_create()}
            SET CONTENT = {cent}, STATUS = {sta}
            WHERE ID = {num}
            ''')

    
    def sql_fetchall(self):
        pass

    def sql_send(self):
        self.conn.commit()


    def sql_close(self):
        self.conn.close()

def now_plat():
    pat = sys.platform
    act = 'clear' if pat == 'linux' else 'cls'
    os.system(act)

### 界面 ###




while True:
    print('=========================')
    print()
    print(f"\tTheTodo")
    print()
    print('=========================')
    print()
    print('0. 選擇清單')
    print('1. 建立清單')
    print('2. 修改清單')
    print('3. 刪除清單')
    print('4. 結束程式')
    print()
    print('=========================')
    print()
    data = ToDoDate('todo.db')
    print()
    print('=========================')
    print()

    try:
        cho = input('選擇功能：')
        if cho == '0':
            pass
        
        elif cho == '1':
            name = input('請輸入清單名稱：')
            data.sql_create(name)
            data.sql_send()
            now_plat()

        elif cho == '2':
            old = input('請輸入舊清單名稱：')
            new = input('請輸入欲更改名稱：')
            data.sql_alter(old, new)
            data.sql_send()
            now_plat()

        elif cho == '3':
            tab = input('請輸入清單名稱：')
            data.sel_deltab(tab)
            now_plat()

        elif cho == '4':
            break
        else:
            break
    except:
        pass
    finally:
        data.sql_close()