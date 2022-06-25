from PyQt5.QtWidgets import QTextEdit
from login import Login


class Msg(QTextEdit):

    def __init__(self, hei):
        super().__init__()
        print("INIT MSG")
        self.setReadOnly(True)
        self.setFixedHeight(hei)

    # 텍스트 추가
    def add_msg(self, who, text: str):
        # 어디서 보내온 메시지 인지 확인
        if isinstance(who, Login):
            text = "LOGIN : " + text

        # 텍스트 에디트에 메시지 추가
        self.append(text)