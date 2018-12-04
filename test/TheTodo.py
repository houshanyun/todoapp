import os
import sys
import sqlite3 as sq3
from datetime import datetime, timedelta
import time

### 界面 ###

def now_plat():
    pat = sys.platform
    act = 'clear' if pat == 'linux' else 'cls'
    os.system(act)


def display_list():
    print('===========================================================')
    print()

    print("TheTodo")

    print()
    print('===========================================================')
    print()
    print('0. 選擇清單')
    print('1. 建立清單')
    print('2. 修改清單')
    print('3. 刪除清單')
    print('4. 結束程式')
    print()
    print('===========================================================')


def display_todo():
    print('===========================================================')
    print()

    print("TheTodo")

    print()
    print('===========================================================')
    print()
    print('0. 回到上層')
    print('1. 建立項目')
    print('2. 修改項目')
    print('3. 刪除項目')
    print('4. 完成項目')
    print('5. 清除完成')    
    print('6. 結束程式')
    print()
    print('===========================================================')

### 功能函數 ###

class ToDoDate:

    nowdir = os.path.abspath(os.path.dirname(__file__))
    dbname = '/'.join([nowdir, 'todo.db'])
    tablist = list()
    
    def __init__(self):
        '''

        SQLite會自動維護一個系統表單「sqlite_master」，
        裡面會有我們創建的表單信息。

        '''
        self.conn = sq3.connect(self.dbname)

        
    def sql_update(self):
        self.conn.commit()
        self.cur = self.conn.execute('SELECT * FROM sqlite_master')
        self.table_rows = self.cur.fetchall()
        

    def table_view(self):
        self.sql_update()
        now_plat()
        display_list()
        func = lambda x : x != 'sqlite_sequence'
        L = [row[1] for row in self.table_rows] 
        self.tablist = [r for r in filter(func, L)]
        if len(self.tablist) > 0:    
            print('===========================================================')
            print()
            for dex, tab in enumerate(self.tablist):
                    print(f'{dex:02}. {tab}')
            print()
            print('===========================================================')
            print()
        else:
            print('===========================================================')
            print()
            print('尚未建立清單！')
            print()
            print('===========================================================')
            print()
        switch_list()
        
    
    def sql_create(self):    
        name = input('請輸入清單名稱：')
        if name.isalnum():
            self.conn.execute(
                f'''CREATE TABLE {name} (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    CONTENT TEXT,
                    NOWDATE TEXT,
                    COMPLETE TEXT,
                    STATUS TEXT
                )''' )
            self.table_view()
        else:
            print()
            print('<-請輸入正確名稱！->')
            print()
            self.sql_create()
            

    def sql_alter(self):
        old = input('請輸入舊清單名稱：')
        new = input('請輸入欲更改名稱：')
        if old in self.tablist:
            self.conn.execute(
                f'''ALTER TABLE '{old}'
                RENAME TO '{new}' '''
            )
            self.table_view()
        else:
            print()
            print('<-清單不存在！->')
            print()
            self.sql_alter()

    def sql_deltab(self):
        tab = input('請輸入清單名稱：')
        if tab in self.tablist:
            self.conn.execute(f"DROP TABLE '{tab}'")
            self.table_view()
        else:
            print()
            print('<-清單不存在！->')
            print()
            self.sql_deltab()
            

    def choice_tab(self):
        if len(self.tablist) > 0:
            cur = self.change_item()
            cur.send(None)
            print()
            tab_name = input('請選擇清單：')
            if tab_name not in self.tablist:
                print()
                print('<-清單不存在！->')
                print()
                self.choice_tab()
            else:    
                cur.send(tab_name)
        else:    
            print()
            print('<-請先建立清單！->')
            print()
            switch_list()
            

    def change_item(self):
        tab_name = yield
        cur = self.conn.execute(f'SELECT * FROM {tab_name}')
        rows = cur.fetchall()
        now_plat()
        display_todo()
        print(tab_name)
        print('===========================================================')
        print('編號', '項目', '\t建立時間', '完成時間',sep='\t')
        print('===========================================================')
        for dex, tab, date, complete, _ in rows:
            print(f"{dex:03} : {tab:10.8s}\t{date:13}\t{complete}")
        print()
        print('===========================================================')
        print()
        switch_todo(tab_name)
        

    def sql_send(self):
        self.conn.commit()


    def sql_close(self):
        self.conn.close()


class Cho_Item(ToDoDate):
    def __init__(self):
        super().__init__()
        self.tab_name = None
    
    def set_tab(self, name):
        self.tab_name = name
        

    def item_update(self):
        self.conn.commit()
        self.tab_cur = self.conn.execute(f'SELECT * FROM {self.tab_name}')
        self.item_rows = self.tab_cur.fetchall()
        self.id_rows = [i for i, _, _, _, _ in self.item_rows]


    def view(self):
        self.item_update()
        now_plat()
        display_todo()
        print(self.tab_name)
        print('===========================================================')
        print('編號', '項目', '\t建立時間', '完成時間',sep='\t')
        print('===========================================================')
        for dex, tab, date, complete, _ in self.item_rows:
            print(f"{dex:03} : {tab:10.8s}\t{date:13}\t{complete}")
        print()
        print('===========================================================')
        print()
        switch_todo(self.tab_name)


    def sql_insert(self):
        dt = datetime.now()
        nowdate = dt.strftime('%F')
        content = input('請輸入待辦事項：')
        if not content:
            print()
            print('<-請輸入內容！->')
            print()
            self.sql_insert()
        else:
            self.conn.execute(
                f'''INSERT INTO {self.tab_name} (CONTENT, NOWDATE, STATUS)
                VALUES ('{content}', '{nowdate}', 0)''')
            self.view()
        
    
    def sql_edit(self):
        self.item_update()
        num = int(input('項目編號：'))
        content = input('修改內容：')
        if (num in self.id_rows) and content:
            self.conn.execute(
                f'''UPDATE {self.tab_name}
                SET CONTENT = '{content}'
                WHERE ID = {num}
                ''')
            self.view()
        else:
            print()
            print('<-項目編號不存在或輸入正確內容！->')
            print()
            self.sql_edit()
    

    def sql_complete(self):
        self.item_update()
        dt = datetime.now()
        nowdate = dt.strftime('%F')
        num = int(input('項目編號：'))
        if num in self.id_rows:
            self.conn.execute(
                f'''UPDATE {self.tab_name}
                SET COMPLETE = '{nowdate}', STATUS = 1
                WHERE ID = {num}
                ''')
            self.view()
        else:
            print()
            print('<-項目編號不存在！->')
            print()
            self.sql_complete()

    
    def sql_delcomp(self):
        act = input('確定刪除請輸入y,若否則n：')
        if act == 'y':
            self.conn.execute(f'DELETE FROM {self.tab_name} WHERE STATUS = 1')
        self.view()

    
    def sql_delitem(self):    
        self.item_update()
        num = int(input('項目編號：'))
        if  num in self.id_rows:
            self.conn.execute(f"DELETE FROM {self.tab_name} WHERE ID = '{num}'")
            self.view()
        else:
            print()
            print('<-項目編號不存在！->')
            print()
            self.sql_delitem()


def switch_list():
    list_dict = {
        '0': data.choice_tab,
        '1': data.sql_create,
        '2': data.sql_alter,
        '3': data.sql_deltab,
        '4': sys.exit
    }
    num = input('選擇功能:')
    if num in '01234':
        return list_dict.get(num, sys.exit)()
    else:
        print()
        print('請輸入0~4的數字！')
        print()
        switch_list()


def switch_todo(name):
    cho_data.set_tab(name)
    todo_dict = {
        '0': data.table_view,
        '1': cho_data.sql_insert,
        '2': cho_data.sql_edit,
        '3': cho_data.sql_delitem,
        '4': cho_data.sql_complete,
        '5': cho_data.sql_delcomp,
        '6': sys.exit
    }
    id_num = input('選擇功能:')
    if id_num in '0123456':
        return todo_dict.get(id_num, sys.exit)()
    else:
        print()
        print('請輸入0~6的數字！')
        print()
        switch_todo(name)
        

def main():
    display_list()
    data.table_view()


### main ###

data = ToDoDate()
cho_data = Cho_Item()

try:
    main()

except SystemExit:
    print()
    print('<-請輸入正確格式的整數！->')
    print()
    time.sleep(1)
    main()

except Exception as e:
    print(e)

finally:
    data.sql_close()

