"""
작성자 : 외기러기
최초 작성 시작 : 2024-05-03
최근 작성 완료 : 2026-05-31
내가 만든 이 코드를 당신 또는 다른사람이 먼저 만들었다고 거짓말하지 마세요!!
"""


from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from traceback import format_exc

from organs.Logger import logger
from organs.AccountList import AccountList
from organs.PswdSettings import PasswordSettings


# 앱 전체를 나타내는 클래스
class PswdMakerApp(App):
    # 앱을 그린다
    def build(self):
        Builder.load_file('./felises/AccountList.kv')
        Builder.load_file('./felises/PasswordSettings.kv')

        self.__accountListScreen = AccountList()
        self.__pswdSettingsScreen = PasswordSettings()
        
        self.__mainScreen = ScreenManager()
        self.__mainScreen.add_widget(self.__accountListScreen)
        self.__mainScreen.add_widget(self.__pswdSettingsScreen)

        return self.__mainScreen

if __name__ == "__main__":
    try:
        PswdMakerApp().run()
    except:
        logger.critical(format_exc())
