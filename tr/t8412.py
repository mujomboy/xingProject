
import pythoncom
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QPushButton, QTableWidgetItem, QTableWidget, QVBoxLayout, QHBoxLayout, QLabel, \
    QLineEdit
from admin import Conn
from event.query import QueryEvents

# 주식챠트(N분)데이터 조회
class t8412(QWidget):

    def __init__(self):
        super().__init__()

        self.mainLayout = QVBoxLayout(self)     # 레이아웃 생성 및 위젯 연결
        self.subLayout = QHBoxLayout()          # 서브 레이아웃 생성

        self.btn = QPushButton("조회")            # 조회 버튼
        self.btn.setFixedWidth(100)             # 버튼 가로 길이 고정

        lbl_code = QLabel("      종목코드 : ")     # 종목코드 라벨
        lbl_n_min = QLabel("      (N)분 : ")  # (N)분 라벨
        lbl_sdate = QLabel("      시작날짜 : ")  # 시작날짜 라벨
        lbl_edate = QLabel("      종료날짜 : ")  # 종료날짜 라벨

        self.txt_code = QLineEdit("")    # 종목코드 에디트 생성
        self.txt_n_min = QLineEdit("")  # (N)분 에디트 생성
        self.txt_sdate = QLineEdit("")  # 시작날짜 에디트 생성
        self.txt_edate = QLineEdit("")  # 종료날짜 에디트 생성
        self.txt_n_min.setPlaceholderText("ex) 5")
        self.txt_sdate.setPlaceholderText("ex) 20220701")
        self.txt_edate.setPlaceholderText("ex) 20220701")

        self.table = QTableWidget()             # 데이터를 삽입할 테이블 위젯 생성
        self.table.setColumnCount(8)            # 항목 개수 지정
        self.table.setHorizontalHeaderLabels([
            "날짜"
            , "시간"
            , "시가"
            , "고가"
            , "저가"
            , "종가"
            , "거래량"
            , "거래대금"
        ]) # 테이블 항목명

        self.mainLayout.addLayout(self.subLayout)   # 메인레이아웃에 서브 레이아웃 배치
        self.mainLayout.addWidget(self.table)       # 메인레이아웃에 테이블 레이아웃 배치

        self.subLayout.addWidget(lbl_code)  # 서브레이아웃에 라벨 배치
        self.subLayout.addWidget(self.txt_code)  # 서브레이아웃에 에디트 배치
        self.subLayout.addWidget(lbl_n_min)  # 서브레이아웃에 라벨 배치
        self.subLayout.addWidget(self.txt_n_min)  # 서브레이아웃에 에디트 배치
        self.subLayout.addWidget(lbl_sdate)  # 서브레이아웃에 라벨 배치
        self.subLayout.addWidget(self.txt_sdate)  # 서브레이아웃에 에디트 배치
        self.subLayout.addWidget(lbl_edate)  # 서브레이아웃에 라벨 배치
        self.subLayout.addWidget(self.txt_edate)  # 서브레이아웃에 에디트 배치


        self.subLayout.addWidget(self.btn, alignment=Qt.AlignRight)          # 서브레이아웃에 버튼 배치

        # 조회 버튼 클릭 시 호출할 함수 연결
        self.btn.clicked.connect(self.btn_clicked)

    # 조회 버튼 클릭 시 호출 함수
    def btn_clicked(self):

        # 쿼리 이벤트 객체 가져오기
        query = Conn().get_query()

        # 주식챠트(N분)데이터 조회에 해당되는 t8412.res 파일이 있는 경로 가져오기
        resfile_path = Conn().get_res_path("t8412")

        # 조회 시 입력 파라미터 타입 명 t8412InBlock
        inblock = "%sInBlock" % "t8412"
        # 조회 시 리턴 파라미터 타입 명 t8412InBlock
        outblock1 = "%sOutBlock1" % "t8412"

        # 경로를 통해 res 파일를 로드.
        query.LoadFromResFile(resfile_path)
        # 입력 파리미터를 초기화 합니다.
        query.SetFieldData(inblock, "shcode", 0, self.txt_code.text())      # 종목코드
        query.SetFieldData(inblock, "ncnt", 0, self.txt_n_min.text())  # (N)분
        query.SetFieldData(inblock, "sdate", 0, self.txt_sdate.text())  # 시작날짜
        query.SetFieldData(inblock, "edate", 0, self.txt_edate.text())  # 종료날짜
        query.SetFieldData(inblock, "comp_yn", 0, "N")  # 압축여부

        # 조회 요청
        query.Request(0)

        while not QueryEvents.state:
            # 응답 대기
            pythoncom.PumpWaitingMessages()

        # 응답이 왔으므로 응답 대기 관련 state 값 초기화
        QueryEvents.state = not QueryEvents.state

        # 리턴 해온 데이터 수 만큼 테이블 로우 개수를 초기화 해줍니다.
        self.table.setRowCount(query.GetBlockCount(outblock1))

        for i in range(query.GetBlockCount(outblock1)):
            # 리턴 데이터 추출
            date = query.GetFieldData(outblock1, "date", i).strip()             # 날짜
            time = query.GetFieldData(outblock1, "time", i).strip()             # 시간
            open = query.GetFieldData(outblock1, "open", i).strip()             # 시가
            high = query.GetFieldData(outblock1, "high", i).strip()             # 고가
            low = query.GetFieldData(outblock1, "low", i).strip()               # 저가
            close = query.GetFieldData(outblock1, "close", i).strip()           # 종가
            jdiff_vol = query.GetFieldData(outblock1, "jdiff_vol", i).strip()   # 거래량
            value = query.GetFieldData(outblock1, "value", i).strip()           # 거래대금


            # 테이블에 데이터 삽입
            self.table.setItem(i, 0, QTableWidgetItem(date))
            self.table.setItem(i, 1, QTableWidgetItem(time))
            self.table.setItem(i, 2, QTableWidgetItem(open))
            self.table.setItem(i, 3, QTableWidgetItem(high))
            self.table.setItem(i, 4, QTableWidgetItem(low))
            self.table.setItem(i, 5, QTableWidgetItem(close))
            self.table.setItem(i, 6, QTableWidgetItem(jdiff_vol))
            self.table.setItem(i, 7, QTableWidgetItem(value))

