import pythoncom
from PyQt5.QtChart import QChart, QChartView, QCandlestickSeries, QCandlestickSet, QDateTimeAxis, QValueAxis, \
    QLineSeries
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen, QBrush
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

        self.chart_view = QChartView()
        self.chart_view.setRenderHint(QPainter.Antialiasing)

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

        print(query.state, code)

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
        query.state = False

        # 데이터 가공
        Conn().get_data().init_t8412(query, outblock1)

        chart = QChart()  # 차트 생성
        chart.legend().hide()

        ma_list = [5, 15, 30, 60]
        color_list = [Qt.red, Qt.green, Qt.blue, Qt.yellow]

        for i in range(len(ma_list)):

            # 라인 시리즈 생성
            line_series = QLineSeries()

            pen = QPen()
            pen.setWidth(2)
            pen.setColor(color_list[i])
            line_series.setPen(pen)

            for list in Conn().get_data().get_t8412_avg_list(ma_list[i]):
                line_series.append(list[1], list[0])

            # 시리즈 연결
            chart.addSeries(line_series)

        # 캔들 시리즈 생성
        candle_series = QCandlestickSeries()  # 캔들스틱 시리즈
        candle_series.setIncreasingColor(Qt.red)  # 상승시 색상
        candle_series.setDecreasingColor(Qt.blue)  # 하락시 색상
        candle_series.setBodyWidth(.8)

        for list in Conn().get_data().get_t8412_candle_list():
            candle_series.append(QCandlestickSet(float(list[0]), float(list[1]), float(list[2]), float(list[3]), float(list[4])))

        # 시리즈 연결
        chart.addSeries(candle_series)
        chart.createDefaultAxes()

        self.chart_view.setChart(chart)


