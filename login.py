import pythoncom
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QLineEdit, QPushButton, QRadioButton

from admin import Conn

class Login(QWidget):

    def __repr__(self):
        return "LOGIN"

    def __init__(self):
        super().__init__()
        print("INIT LOGIN")
        self.layout_main = QHBoxLayout(self)  # 메인레이아웃

        lbl_id = QLabel("ID ")               # 아이디 라벨 생성
        lbl_pw = QLabel("PW ")               # 패스워드 라벨 생성
        lbl_port = QLabel("PORT ")           # 포트 라벨 생성
        lbl_cert = QLabel("CERTIFICATION ")  # 인증서 라벨 생성

        self.txt_id = QLineEdit("")                 # 아이디 에디트 생성
        self.txt_pw = QLineEdit("")                 # 패스워드 에디트 생성
        self.txt_port = QLineEdit("200001")         # 포트 에디트 생성
        self.txt_cert = QLineEdit()                 # 인증서 에디트 생성

        self.rdo_real = QRadioButton("실제투자")
        self.rdo_vir = QRadioButton("모의투자")
        self.rdo_vir.setChecked(True)

        self.btn_login = QPushButton("LOGIN")    # 로그인 버튼

        lbl_id.setAlignment(Qt.AlignCenter)
        lbl_pw.setAlignment(Qt.AlignCenter)
        lbl_port.setAlignment(Qt.AlignCenter)
        lbl_cert.setAlignment(Qt.AlignCenter)

        # 위젯들 레이아웃에 연결
        self.layout_main.addWidget(lbl_id)
        self.layout_main.addWidget(self.txt_id)
        self.layout_main.addWidget(lbl_pw)
        self.layout_main.addWidget(self.txt_pw)
        self.layout_main.addWidget(lbl_port)
        self.layout_main.addWidget(self.txt_port)
        self.layout_main.addWidget(lbl_cert)
        self.layout_main.addWidget(self.txt_cert)
        self.layout_main.addWidget(self.rdo_real)
        self.layout_main.addWidget(self.rdo_vir)
        self.layout_main.addWidget(self.btn_login)

        # 버튼 클릭 시 호출할 함수 연결
        self.btn_login.clicked.connect(self.login_clicked)

        # 라인에디터 Enter 시 호출할 함수 연결
        self.txt_id.returnPressed.connect(self.login_clicked)
        self.txt_pw.returnPressed.connect(self.login_clicked)

    # 세션 생성
    def create_XASession(self):
        Conn().add_msg(self, "Check XASession state")

        # 세션 객체 생성 여부 확인
        if not Conn().is_session():
            Conn().add_msg(self, "Create XASession")
            # 세션 객체 생성
            Conn().get_session()

        # 서버 연결 여부 확인
        elif Conn().get_session().IsConnected():
            Conn().add_msg(self, "Server is Connected")
            # 서버 끊기
            self.disconnect_server()

    # 서버 끊기
    def disconnect_server(self):
        session = Conn().get_session()
        Conn().add_msg(self, 'Disconnected server')
        session.DisconnectServer()
        session.state = ""
        session.msg = ""

    # 서버 연결
    def connect_server(self):
        Conn().add_msg(self, 'Request server connect')

        # 접속 URL
        url = 'demo.ebestsec.co.kr'  # 모의 투자
        if self.rdo_real.isChecked():
            url = 'hts.ebestsec.co.kr'  # 실제 투자

        Conn().add_msg(self, "URL : " + url)
        Conn().add_msg(self, "PORT : " + self.txt_port.text())

        # 서버 연결 요청 (URL, 포트 번호 전달)
        result = Conn().get_session().ConnectServer(url, int(self.txt_port.text()))

        # 연결 여부 확인
        if not result:
            # 연결 실패 시
            info = self.get_error_info()
            Conn().add_msg(self, "Connect Failed")
            Conn().add_msg(self, "Error Code : " + info[0])
            Conn().add_msg(self, "Error Msg : " + info[1])
            if Conn().get_session().IsConnected():
                self.disconnect_server()

            return False

        Conn().add_msg(self, "Server Connect Success")
        return True

    # 로그인 진행
    def login(self):
        session = Conn().get_session()

        Conn().add_msg(self, "Login Attempt")

        # 이베스트 로그인
        Conn().add_msg(self, "ID : " + self.txt_id.text())
        Conn().add_msg(self, "PWD : " + self.txt_pw.text())
        Conn().add_msg(self, "CERT : " + self.txt_cert.text())

        # 세션 로그인 요청
        session.Login(self.txt_id.text(), self.txt_pw.text(), self.txt_cert.text(), 0, 0)

        Conn().add_msg(self, 'Wait....')
        while session.state == "":
            # 로그인 상태 변경 메시지 채크
            pythoncom.PumpWaitingMessages()

        is_success = False

        if session.state == "0000":
            is_success = True
            Conn().add_msg(self, 'Login Success')
        else:
            Conn().add_msg(self, "Login Failed")
            Conn().add_msg(self, "Error Code : " + session.state)
            Conn().add_msg(self, "Error Msg : " + session.msg)

        Conn().add_msg(self, "========== END =============\n")

        return is_success

    def login_clicked(self):

        # 로그인 진행중... 버튼 비활성화
        self.btn_login.setEnabled(False)

        # 탭 비활성화
        Conn().get_tap().setEnabled(False)

        # 세션 생성
        self.create_XASession()

        # 서버 연결
        if not self.connect_server():
            return

        # 로그인 진행 (성공 시 탭 활성화)
        if self.login():
            Conn().get_tap().setEnabled(True)

        # 로그인 진행완료.. 버튼 활성화
        self.btn_login.setEnabled(True)

    def get_error_info(self):
        code = Conn().get_session().GetLastError()
        return [code, Conn().get_session().GetErrorMessage(code)]


