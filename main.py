import sys

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget

from admin import Conn
from login import Login
from msg import Msg
from tr.t8424 import t8424


class MainScreen(QMainWindow):

    def __init__(self, wid, hei):
        super().__init__()

        self.setWindowTitle("xingAPI Project")  # 프로젝트 타이틀 설정
        self.setGeometry(0, 0, int(wid), int(hei*.9))    # 화면 사이즈 설정

        self.mainWidget = QWidget()                         # 메인 위젯 생성
        self.mainLayout = QVBoxLayout(self.mainWidget)      # 메인 레이아웃 생성 및 메인 위젯 연결
        self.mainTab = QTabWidget()                         # 탭 위젯 생성

        self.mainLayout.addWidget(Login())                  # 로그인 클래스 생성 및 레이아웃에 추가
        self.mainLayout.addWidget(self.mainTab)             # 메인 레이아웃에 텝 위젯 추가
        self.setCentralWidget(self.mainWidget)              # 메인윈도우 센트럴위젯에 메인 위젯 연결

        Conn().set_msg(Msg(int(hei * .15)))  # 메시지 객체 Conn 에 전달
        Conn().set_tap(self.mainTab)  # 탭 객체 Conn 에 전달

        self.mainLayout.addWidget(Conn().get_msg())         # 메시지 클래스 새성 및 레이아웃에 추가

        self.mainTab.setEnabled(False)                      # 탭 비활성화

        self.mainTab.addTab(t8424(), "업종전체조회")                        # 업종전체조회 위젯 추가

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    size: QSize = app.primaryScreen().size()    # 모니터 사이즈

    main = MainScreen(size.width()/2, size.height())
    sys.exit(app.exec_())
