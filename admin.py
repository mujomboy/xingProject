import os.path
import sys

import win32com.client
from event.session import SessionEvents
from event.query import QueryEvents

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

    # SET 메시지 객체
    def set_msg(self, msg):
        self.__msg = msg

    # GET 메시지 객체
    def get_msg(self):
        return self.__msg

    # SET 탭 객체
    def set_tap(self, tap):
        self.__tap = tap

    # GET 탭 객체
    def get_tap(self):
        return self.__tap

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

    # GET 쿼리 객체
    def get_query(self):
        if self.__query is None:
            # 쿼리 객체 요청 및 객체 생성
            self.__query = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", QueryEvents)

        return self.__query

    # res 폴더 경로 리턴
    def get_res_path(self, res_name):
        return "%s\\res\\%s.res" % (os.path.abspath(os.path.dirname(sys.argv[0])), res_name)