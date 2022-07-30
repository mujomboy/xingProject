import pythoncom
from PyQt5.QtChart import QChart, QChartView, QCandlestickSeries, QCandlestickSet, QDateTimeAxis, QValueAxis
from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit

from admin import Conn


class t8412_chart(QWidget):

    def __repr__(self):
        return "주식차트"

    def __init__(self):
        super().__init__()

        self.mainLayout = QVBoxLayout(self)  # 레이아웃 생성 및 위젯 연결
        self.subLayout = QHBoxLayout()  # 서브 레이아웃 생성

        self.btn = QPushButton("조회")  # 조회 버튼
        self.btn.setFixedWidth(100)  # 버튼 가로 길이 고정

        lbl_name = QLabel("      종목명 : ")  # 종목명 라벨
        lbl_n_min = QLabel("      (N)분 : ")  # (N)분 라벨
        lbl_sdate = QLabel("      시작날짜 : ")  # 시작날짜 라벨
        lbl_edate = QLabel("      종료날짜 : ")  # 종료날짜 라벨

        self.txt_name = QLineEdit("삼성전자")  # 종목명 에디트 생성
        self.txt_n_min = QLineEdit("5")  # (N)분 에디트 생성
        self.txt_sdate = QLineEdit("20220714")  # 시작날짜 에디트 생성
        self.txt_edate = QLineEdit("20220714")  # 종료날짜 에디트 생성

        self.txt_n_min.setPlaceholderText("ex) 5")
        self.txt_sdate.setPlaceholderText("ex) 20220701")
        self.txt_edate.setPlaceholderText("ex) 20220701")

        # ========================================== 챠트 ==========================================
        self.chart = QChart()                # 차트
        self.chart.legend().hide()

        self.axis_x = QDateTimeAxis()
        self.axis_x.setFormat("hh:mm:ss")

        self.axis_y = QValueAxis()
        self.axis_y.setLabelFormat("%i")



        self.chart_view = QChartView(self.chart)  # 차트뷰
        self.chart_view.setRenderHint(QPainter.Antialiasing)
        # ========================================== 챠트 ==========================================

        self.mainLayout.addLayout(self.subLayout)  # 메인레이아웃에 서브 레이아웃 배치
        self.mainLayout.addWidget(self.chart_view)           # 메인레이아웃에 차트 배치

        self.subLayout.addWidget(lbl_name)  # 서브레이아웃에 라벨 배치
        self.subLayout.addWidget(self.txt_name)  # 서브레이아웃에 에디트 배치
        self.subLayout.addWidget(lbl_n_min)  # 서브레이아웃에 라벨 배치
        self.subLayout.addWidget(self.txt_n_min)  # 서브레이아웃에 에디트 배치
        self.subLayout.addWidget(lbl_sdate)  # 서브레이아웃에 라벨 배치
        self.subLayout.addWidget(self.txt_sdate)  # 서브레이아웃에 에디트 배치
        self.subLayout.addWidget(lbl_edate)  # 서브레이아웃에 라벨 배치
        self.subLayout.addWidget(self.txt_edate)  # 서브레이아웃에 에디트 배치

        self.subLayout.addWidget(self.btn, alignment=Qt.AlignRight)  # 서브레이아웃에 버튼 배치

        # 조회 버튼 클릭 시 호출할 함수 연결
        self.btn.clicked.connect(self.btn_clicked)
        # 종목명 엔터 시 호출할 함수 연결
        self.txt_name.returnPressed.connect(self.btn_clicked)


    # 조회 버튼 클릭 시 호출 함수
    def btn_clicked(self):

        # 종목코드 정보 가져오기
        code = Conn().get_code(self.txt_name.text())

        Conn().add_msg(self, "조회중..")

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
        query.SetFieldData(inblock, "shcode", 0, code)  # 종목코드
        query.SetFieldData(inblock, "ncnt", 0, self.txt_n_min.text())  # (N)분
        query.SetFieldData(inblock, "sdate", 0, self.txt_sdate.text())  # 시작날짜
        query.SetFieldData(inblock, "edate", 0, self.txt_edate.text())  # 종료날짜
        query.SetFieldData(inblock, "comp_yn", 0, "N")  # 압축여부

        # 조회 요청
        query.Request(0)

        while not query.state:
            # 응답 대기
            pythoncom.PumpWaitingMessages()

        Conn().add_msg(self, query.msg)

        if str(query.error) != '0':
            Conn().add_msg(self, "Error Code : " + query.msgCode)
            Conn().add_msg(self, "Error Msg : " + query.msg)

        Conn().add_msg(self, "========== END =============\n")

        # 응답이 왔으므로 응답 대기 관련 state 값 초기화
        query.state = not query.state

        self.chart.removeAllSeries()

        series = QCandlestickSeries()           # 캔들스틱 시리즈
        series.setIncreasingColor(Qt.red)       # 상승시 색상
        series.setDecreasingColor(Qt.blue)      # 하락시 색상


        for i in range(query.GetBlockCount(outblock1)):
            date = query.GetFieldData(outblock1, "date", i).strip()  # 날짜
            time = query.GetFieldData(outblock1, "time", i).strip()  # 시간
            open = query.GetFieldData(outblock1, "open", i).strip()  # 시가
            high = query.GetFieldData(outblock1, "high", i).strip()  # 고가
            low = query.GetFieldData(outblock1, "low", i).strip()  # 저가
            close = query.GetFieldData(outblock1, "close", i).strip()  # 종가
            dt = QDateTime.fromString(date+time, "yyyyMMddhhmmss")
            series.append(QCandlestickSet(float(open), float(high), float(low), float(close), dt.toMSecsSinceEpoch()))

        self.chart.addSeries(series)  # 시리즈 연결
        self.chart.addAxis(self.axis_x, Qt.AlignBottom)  # x축 좌표 설정
        self.chart.addAxis(self.axis_y, Qt.AlignLeft)  # y축 좌표 설정

        series.attachAxis(self.axis_x)
        series.attachAxis(self.axis_y)
