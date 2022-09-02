
class Data:

    def __init__(self):
        self.t8412_candle_list = [] # 캔들 리스트
        self.t8412_avg_list = []    # 이동평균 리스트


    # 주식차트(N분) 쿼리 등록
    def init_t8412(self, query, outblock1):

        self.t8412_candle_list.clear()


        for i in range(query.GetBlockCount(outblock1)):

            date = query.GetFieldData(outblock1, "date", i).strip()  # 날짜
            time = query.GetFieldData(outblock1, "time", i).strip()  # 시간
            open = query.GetFieldData(outblock1, "open", i).strip()  # 시가
            high = query.GetFieldData(outblock1, "high", i).strip()  # 고가
            low = query.GetFieldData(outblock1, "low", i).strip()  # 저가
            close = query.GetFieldData(outblock1, "close", i).strip()  # 종가

            # 캔들리스트 저장
            self.t8412_candle_list.append([open, high, low, close, i*100000])

    # 캔들 리스트 GET
    def get_t8412_candle_list(self):
        return self.t8412_candle_list

    # 캔들 리스트 GET
    def get_t8412_avg_list(self, ma):
        self.t8412_avg_list.clear()

        # 이동평균리스트 저장
        tmp_list = []
        for i in range(len(self.t8412_candle_list)):
            s = (i - ma) + 1
            e = i + 1

            if s < 0:
                s = 0

            close_list = []
            for j in range(s, e):
                close_list.append(int(self.t8412_candle_list[j][3]))

            tmp_list.append(close_list)

        idx = 0
        for list in tmp_list:
            cnt = len(list)
            sum = 0
            for v in list:
                sum += v

            self.t8412_avg_list.append([sum / cnt, idx * 100000])
            idx += 1

        return self.t8412_avg_list







