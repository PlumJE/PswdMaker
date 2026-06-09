"""
작성자 : 외기러기
최초 작성 시작 : 2026-05-31
최근 작성 완료 : 2026-05-31
내가 만든 이 코드를 당신 또는 다른사람이 먼저 만들었다고 거짓말하지 마세요!!
"""


import logging

from etcetera import rootPath


# logger객체 생성
logger = logging.getLogger()
logger.setLevel(logging.ERROR)

# logger의 로그를 파일에 저장하게 설정
file_handler = logging.FileHandler(rootPath() + '/PswdMaker.log')
logger.addHandler(file_handler)