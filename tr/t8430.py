
import pythoncom
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QPushButton, QTableWidgetItem, QTableWidget, QVBoxLayout, QHBoxLayout
from admin import Conn
from event.query import QueryEvents

# 주식종목조회 클래스
class t8430(QWidget):

    def __init__(self):
        super().__init__()

        self.mainLayout = QVBoxLayout(self)     # 레이아웃 생성 및 위젯 연결
        self.subLayout = QHBoxLayout()          # 서브 레이아웃 생성

        self.btn = QPushButton("조회")            # 조회 버튼
        self.btn.setFixedWidth(100)             # 버튼 가로 길이 고정

        self.table = QTableWidget()             # 데이터를 삽입할 테이블 위젯 생성
        self.table.setColumnCount(4)            # 항목 개수 지정
        self.table.setHorizontalHeaderLabels(["종목명", "종목코드", "구분1", "구분2"]) # 테이블 항목명

        self.mainLayout.addLayout(self.subLayout)   # 메인레이아웃에 서브 레이아웃 배치
        self.mainLayout.addWidget(self.table)       # 메인레이아웃에 테이블 레이아웃 배치
        self.subLayout.addWidget(self.btn, alignment=Qt.AlignRight)          # 서브레이아웃에 버튼 배치

        # 조회 버튼 클릭 시 호출할 함수 연결
        self.btn.clicked.connect(self.btn_clicked)

    # 조회 버튼 클릭 시 호출 함수
    def btn_clicked(self):

        # 쿼리 이벤트 객체 가져오기
        query = Conn().get_query()

        # 주식종목조회에 해당되는 t8430.res 파일이 있는 경로 가져오기
        resfile_path = Conn().get_res_path("t8430")

        # 조회 시 입력 파라미터 타입 명 t8430InBlock
        inblock = "%sInBlock" % "t8430"
        # 조회 시 리턴 파라미터 타입 명 t8430InBlock
        outblock = "%sOutBlock" % "t8430"

        # 경로를 통해 res 파일를 로드.
        query.LoadFromResFile(resfile_path)
        # 입력 파리미터를 초기화 합니다.
        query.SetFieldData(inblock, "gubun", 0, '0')
        # 조회 요청
        query.Request(0)

        while not QueryEvents.state:
            # 응답 대기
            pythoncom.PumpWaitingMessages()

        # 응답이 왔으므로 응답 대기 관련 state 값 초기화
        QueryEvents.state = not QueryEvents.state

        # 리턴 해온 데이터 수 만큼 테이블 로우 개수를 초기화 해줍니다.
        self.table.setRowCount(query.GetBlockCount(outblock))

        for i in range(query.GetBlockCount(outblock)):
            # 리턴 데이터 추출
            name = query.GetFieldData(outblock, "hname", i).strip()
            code = query.GetFieldData(outblock, "shcode", i).strip()
            gubun1 = query.GetFieldData(outblock, "gubun", i).strip()
            gubun2 = query.GetFieldData(outblock, "etfgubun", i).strip()

            # 테이블에 데이터 삽입
            self.table.setItem(i, 0, QTableWidgetItem(name))
            self.table.setItem(i, 1, QTableWidgetItem(code))
            self.table.setItem(i, 2, QTableWidgetItem(gubun1))
            self.table.setItem(i, 3, QTableWidgetItem(gubun2))
