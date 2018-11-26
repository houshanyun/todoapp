import os
import sys
import sqlite3 as sq3
from datetime import datetime
import asyncio

### 界面 ###

def now_plat():
    pat = sys.platform
    act = 'clear' if pat == 'linux' else 'cls'
    os.system(act)


def display_list():
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


def display_todo():
    print('=========================')
    print()

    print(f"\tTheTodo")

    print()
    print('=========================')
    print()
    print('0. 選擇項目')
    print('1. 建立項目')
    print('2. 修改項目')
    print('3. 刪除項目')
    print('4. 清除完成')
    print('5. 回到上層')
    print('5. 結束程式')
    print()
    print('=========================')

### 功能函數 ###

class ToDoDate:

    def __init__(self, dbname):
        '''

        SQLite會自動維護一個系統表單「sqlite_master」，
        裡面會有我們創建的表單信息。

        '''
        self.conn = sq3.connect(dbname)
        
        #self.table_rows = self.cur.fetchall()
        self.func = lambda x : x != 'sqlite_sequence'
        self.tablist =list()
        self.name = None
        
    
    def table_view(self):
        cur = self.conn.execute('SELECT * FROM sqlite_master')
        table_rows = cur.fetchall()
        now_plat()
        display_list()
        if table_rows: 
            for r in filter(self.func, [row[1] for row in table_rows]):
                self.tablist.append(r)
            print('=========================')
            print()
            for dex, tab in enumerate(self.tablist):
                    print(f'{dex:02}. {tab}')
            print()
            print('=========================')
            print()
            self.tablist.clear()
        else:
            print('尚未建立清單！')
        
        switch_list()
        
    
    def sql_create(self):
        name = input('請輸入清單名稱：')
        self.conn.execute(
            f'''CREATE TABLE {name} (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                CONTENT TEXT,
                DATE TEXT,
                STATUS TEXT
            )''' )
        self.conn.commit()
        self.table_view()
            

    def sql_alter(self):
        old = input('請輸入舊清單名稱：')
        new = input('請輸入欲更改名稱：')
        self.conn.execute(
            f'''ALTER TABLE '{old}'
            RENAME TO '{new}' '''
        )
        self.conn.commit()
        self.table_view()
        

    def sel_deltab(self):
        tab = input('請輸入清單名稱：')
        self.conn.execute(f'DROP TABLE {tab}')
        self.conn.commit()
        self.table_view()


    def choice_tab(self):
        cur = self.item_view()
        print(cur)
        cur.send(None)
        tab_name = input('請選擇清單：')
        cur.send(tab_name)


    def item_view(self):
        tab_name = yield
        cur = self.conn.execute(f'SELECT * FROM {tab_name}')
        rows = cur.fetchall()
        now_plat()
        display_todo()
        print(tab_name)
        print('=========================')
        print()
        for dex, tab, date, _ in rows:
            print(dex, tab, date)
        print()
        print('=========================')
        print()
        switch_todo(tab_name)
        

    def sql_send(self):
        self.conn.commit()


    def sql_close(self):
        self.conn.close()


class Cho_Item(ToDoDate):
    def __init__(self, dbname):
        super().__init__(dbname)
        self.tab_name = None
    

    def view(self):
        cur = self.conn.execute(f'SELECT * FROM {self.tab_name}')
        rows = cur.fetchall()
        now_plat()
        display_todo()
        print(self.tab_name)
        print('=========================')
        print()
        for dex, tab, date, _ in rows:
            print(dex, tab, date)
        print()
        print('=========================')
        print()
        switch_todo(self.tab_name)


    def sql_insert(self, name):
        #name = input('請輸入清單名稱：')
        self.name = name
        item = input('請輸入待辦事項：')
        dt = datetime.now()
        nowdate = dt.strftime('%F')
        #self.name = name
        self.conn.execute(
            f'''INSERT INTO {name} (CONTENT, DATE, STATUS)
            VALUES ('{item}', '{nowdate}', 0)''')
        self.conn.commit()
        self.view()
        
    
    def sql_update(self, name):
        #name = input('清單名稱：')
        num = int(input('項目編號：'))
        cent = input('修改內容：')
        
        self.conn.execute(
            f'''UPDATE {name}
            SET CONTENT = '{cent}'
            WHERE ID = {num}
            ''')
        self.conn.commit()
        self.name = name
        self.view()


def switch_list():
    num = input('選擇功能:')
    list_dict = {
        '0': data.choice_tab,
        '1': data.sql_create,
        '2': data.sql_alter,
        '3': data.sel_deltab,
        '4': sys.exit
    }
    
    return list_dict.get(num, sys.exit)()

def switch_todo(name):
    id_num = input('選擇功能:')
    todo_dict = {
        #0: pass,
        '1': cho_data.sql_insert,
        '2': cho_data.sql_update,
        #3: pass,
        #4: pass,
        #5: pass,
        '6': sys.exit
    }
    return todo_dict.get(id_num, sys.exit)(name)

### main ###

nowdir = os.path.abspath(os.path.dirname(__file__))
data = ToDoDate('/'.join([nowdir, 'todo.db']))
cho_data = Cho_Item('/'.join([nowdir, 'todo.db']))

try:
    display_list()
    data.table_view()
            
except Exception as e:
    print(e)
    
finally:
    data.sql_close()

