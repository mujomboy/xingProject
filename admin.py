

class Conn:

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_ins"):
            cls._ins = super().__new__(cls)

        return cls._ins

    # SET 메시지 객체
    def set_msg(self, msg):
        self.__msg = msg

    # GET 메시지 객체
    def get_msg(self):
        return self.__msg

    # SET 세션 객체
    def set_session(self, session):
        self.__session = session

    # GET 세션 객체
    def get_session(self):
        return self.__session
