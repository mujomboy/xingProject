from PyQt5.QtWidgets import QTextEdit

class Msg(QTextEdit):

    def __init__(self, hei):
        super().__init__()
        print("INIT MSG")
        self.setReadOnly(True)
        self.setFixedHeight(hei)

    # 텍스트 추가
    def add_msg(self, who, text: str):

        name = str(who)
        text = name + " : " + text

        # 텍스트 에디트에 메시지 추가
        self.append(text)