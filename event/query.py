
# 쿼리 클래스
class QueryEvents:

    state = False
    code = ""

    error = ""
    msgCode = ""
    msg = ""

    def OnReceiveData(self, code):
        QueryEvents.code = code
        QueryEvents.state = True

    def OnReceiveMessage(self, error, msgCode, msg):
        QueryEvents.error = error
        QueryEvents.msgCode = msgCode
        QueryEvents.msg = msg