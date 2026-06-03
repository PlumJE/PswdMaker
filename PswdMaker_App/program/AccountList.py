"""
작성자 : 외기러기
최초 작성 시작 : 2026-05-31
최근 작성 완료 : 2026-05-31
내가 만든 이 코드를 당신 또는 다른사람이 먼저 만들었다고 거짓말하지 마세요!!
"""


from pathlib import Path
from random import choice
from functools import partial
from sqlite3 import connect
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import Screen


# 비밀번호 자동생성 및 관리하는 클래스
class AccountList(Screen):
    __dbFilePath = str(Path(__file__).resolve().parent.parent) + '/database/accountList.sqlite3'
    name = 'accountList'

    # 테이블이 있는지 확인하고 없으면 생성한다
    def __ensure_table(self):
        with connect(self.__dbFilePath) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS accountList (
                    num INTEGER PRIMARY KEY AUTOINCREMENT,
                    addr TEXT NOT NULL,
                    acc_id TEXT,
                    pswd TEXT
                )
            """)
            connection.commit()

    # 계정을 새로 생성한다
    def createAccount(self, **kwargs):
        self.__ensure_table()
        with connect(self.__dbFilePath) as connection:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO accountList (addr, acc_id, pswd) VALUES (?, ?, ?)", ('', '', ''))
            connection.commit()
        self.loadAccountList()

    # 계정을 삭제한다
    def deleteAccount(self, **kwargs):
        with connect(self.__dbFilePath) as connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM accountList WHERE num=(SELECT MAX(num) FROM accountList)")
            connection.commit()
        self.loadAccountList()

    # 계정 목록을 불러온다
    def loadAccountList(self, **kwargs):
        self.__ensure_table()
        with connect(self.__dbFilePath) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT num, addr, acc_id, pswd FROM accountList ORDER BY num")
            rows = cursor.fetchall()

        self.ids.accountList.clear_widgets()
        for num, addr, acc_id, pswd in rows:
            ti_addr = TextInput(text=addr or '', multiline=False)
            ti_addr._num = num
            ti_addr._col = 'addr'
            ti_addr.bind(focus=partial(self.saveAccountList, num, 'addr'))
            self.ids.accountList.add_widget(ti_addr)

            ti_id = TextInput(text=acc_id or '', multiline=False)
            ti_id._num = num
            ti_id._col = 'acc_id'
            ti_id.bind(focus=partial(self.saveAccountList, num, 'acc_id'))
            self.ids.accountList.add_widget(ti_id)

            ti_pswd = TextInput(text=pswd or '', multiline=False)
            ti_pswd._num = num
            ti_pswd._col = 'pswd'
            ti_pswd._is_pswd = True
            ti_pswd.bind(focus=partial(self.saveAccountList, num, 'pswd'))
            self.ids.accountList.add_widget(ti_pswd)

    # 입력이 끝난 계정을 저장한다
    def saveAccountList(self, num, column, instance, focused):
        if focused:
            return

        if column not in ('addr', 'acc_id', 'pswd'):
            return
        
        value = instance.text
        with connect(self.__dbFilePath) as connection:
            cursor = connection.cursor()
            # 컬럼명은 화이트리스트로 검증했으므로 안전하게 포맷
            cursor.execute(f"UPDATE accountList SET {column}=? WHERE num=?", (value, num))
            connection.commit()

    # 랜덤한 비밀번호를 생성한다
    def generatePassword(self, **kwargs):
        candidates = self.manager.get_screen('pswdSettings').getPswdCandidates()
        length = self.manager.get_screen('pswdSettings').getLength()
        password = ''.join(choice(candidates) for _ in range(length))

        # 포커스된 위젯을 찾아 그 행의 번호(num) 추출
        focused_num = None
        for w in self.ids.accountList.children:
            if getattr(w, 'focus', False):
                focused_num = getattr(w, '_num', None)
                break
        
        # 포커스된 행의 3번째 열(pswd) 위젯 찾아 password 입력 및 저장
        if focused_num is not None:
            for w in self.ids.accountList.children:
                if getattr(w, '_num', None) == focused_num and getattr(w, '_col', None) == 'pswd':
                    w.text = password
                    with connect(self.__dbFilePath) as connection:
                        cursor = connection.cursor()
                        cursor.execute("UPDATE accountList SET pswd=? WHERE num=?", (password, focused_num))
                        connection.commit()
                    break

        return password
