# 세션 클래스
class SessionEvents:

    state = ""
    msg = ""

    def OnLogin(self, code, msg):
        SessionEvents.state = code
        SessionEvents.msg = msg

    def OnLogout(self):
        print("OnLogout")

    def OnDisconnect(self):
        print("OnDisconnect")