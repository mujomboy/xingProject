# 세션 클래스
class SessionEvents:

    def __init__(self):
        self.state = ""
        self.msg = ""

    def OnLogin(self, code, msg):
        self.state = code
        self.msg = msg

    def OnLogout(self):
        print("OnLogout")

    def OnDisconnect(self):
        print("OnDisconnect")