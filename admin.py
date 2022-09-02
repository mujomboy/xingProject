import os.path
import sys

import win32com.client

from data import Data
from event.query import QueryEvents
from event.session import SessionEvents


class Conn:

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_ins"):
            cls._ins = super().__new__(cls)

        return cls._ins

    def __init__(self):
        if not hasattr(self, "_conn"):
            self._conn = None
            self.__session = None
            self.__query = None
            self.__msg = None

            self.__dic = {}

            self.__t8430 = None

            self.__data = Data()

    # =========================================== MSG ===============================================

    # SET 메시지 객체
    def set_msg(self, msg):
        self.__msg = msg

    # 메시지 등록
    def add_msg(self, who, msg):
        self.__msg.add_msg(who, msg)

    # =========================================== TAP ===============================================
    # SET 탭 객체
    def set_tap(self, tap):
        self.__tap = tap

    # GET 탭 객체
    def get_tap(self):
        return self.__tap

    # =========================================== SESSION ===============================================
    # 세션 객체 생성 여부확인 : 생성 True, 미생성 False
    def is_session(self):
        if self.__session is None:
            return False

        return True

    # GET 세션 객체
    def get_session(self):
        if not self.is_session():
            # 세션 객체 요청 및 객체 생성
            self.__session = win32com.client.DispatchWithEvents("XA_Session.XASession", SessionEvents)

        return self.__session

    # =========================================== QUERY ===============================================
    # GET 쿼리 객체
    def get_query(self):
        if self.__query is None:
            # 쿼리 객체 요청 및 객체 생성
            self.__query = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", QueryEvents)

        return self.__query

    # res 폴더 경로 리턴
    def get_res_path(self, res_name):
        return "%s\\res\\%s.res" % (os.path.abspath(os.path.dirname(sys.argv[0])), res_name)

    # =========================================== 종목명, 종목코드 ===============================================
    # 클리어 dic
    def clear_items(self):
        self.__dic.clear()

    # SET DATA
    def set_items(self, key, value):
        self.__dic[key] = value

    # RETURN CODE
    def get_code(self, key):
        # 종목 정보 없을때 조회 해 오기
        if len(self.__dic) == 0:
            self.__t8430.btn_clicked()

        if self.__dic.__contains__(key):
            return self.__dic[key]
        else:
            print("????")

        return ""

    # =========================================== TR ===============================================
    # t8430 종목 조회 클래스
    def set_t8430(self, tr):
        self.__t8430 = tr

    # =========================================== DATA ===============================================
    def get_data(self):
        return self.__data