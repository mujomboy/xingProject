
# 쿼리 클래스
class QueryEvents:

    def __init__(self):
        self.state = False
        self.code = ""

        self.error = ""
        self.msgCode = ""
        self.msg = ""

    def OnReceiveData(self, code):
        self.code = code
        self.state = True

    def OnReceiveMessage(self, error, msgCode, msg):
        self.error = error
        self.msgCode = msgCode
        self.msg = msg
