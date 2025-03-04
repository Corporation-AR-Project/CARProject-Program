# calculator.py
from data_process import DataProcess
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

# 계산
class Calculator : 
    def __init__(self, link):
        dp = DataProcess(link)
        self.company_info = dp.company_info
        self.company_type = dp.company_type

    # 배열 안에 넣어서 반환
    def return_arr(self, data) :
        return [int(data)]

    # 계산할 수 있는 상태인지 체크
    def calc_check(self, name, year_list) :
        flag = False
        if self.company_info.get(name) : # self.company안에 값이 있고
            key_list = list(self.company_info[name].keys())
            if str(year_list[0]) in key_list and str(year_list[-1]) in key_list : # year_list 값이 안에 다 있는 경우
                flag = True

        return flag

    # 기업의 년도 목록 가져오기
    def company_year_list(self, name) :
        data = [] # 빈배열 세팅
        if self.company_info.get(name) : # company_info 내에 값이 잇는 경우에만
            for key in list(self.company_info[name].keys()) : # 키 배열로 리스트 만들어서 주기
                if not key in ["데이터분류", "업종", "업종명", "종목코드"] : # 데이터 분류, 업종, 업종명, 종목코드는 제외 하고
                    data.append(key) # 배열안에 넣기
        return data

    # 기업 재무 정보 계산 및 분석
    def calc(self, name, year_list) : 
        result = {}
        data = self.company_info[name] # 기업 데이터 가져와서
        type_code = data['업종'] # 업종코드
        type_name = data['업종명'] # 업종명
        jongmok = data['종목코드'] # 종목코드

        # 2014, 2024, 2025 년도 데이터 예측 추가 (2015 ~ 2023 데이터가 전부 있을때 한정)
        if len(year_list) == 9 :
            df = pd.DataFrame(data)
            df = df.iloc[:, ~df.columns.isin(['데이터분류', '업종', '업종명', "종목코드"])]
            x_i = list(df.index)
            year_add_data = {
                '2014' : { "data" : [], "index" : [] },
                '2024' : { "data" : [], "index" : [] },
                '2025' : { "data" : [], "index" : [] }
            }
            df = df.fillna(0)
            # 컬럼별 데이터 추가
            for x in range(len(x_i)) :
                d = df.iloc[x, :] # 데이터 추출
                d = d.fillna(0) # 결측치 제거
                x_data = list(map(self.return_arr, list(d.index))) # x 데이터 추출
                y_data = d.values # y 데이터 추출
                reg = LinearRegression() # 선언
                reg.fit(x_data, y_data) # 
                y_pred = reg.predict([[2014], [2024], [2025]])
                year_add_data['2014']['data'].append(int(float(format(y_pred[0], 'f'))))
                year_add_data['2014']['index'].append(x_i[x])
                year_add_data['2024']['data'].append(int(float(format(y_pred[1], 'f'))))
                year_add_data['2024']['index'].append(x_i[x])
                year_add_data['2025']['data'].append(int(float(format(y_pred[2], 'f'))))
                year_add_data['2025']['index'].append(x_i[x])
            df['2014'] = pd.Series(year_add_data['2014']['data'], index=year_add_data['2014']['index'])
            df['2024'] = pd.Series(year_add_data['2024']['data'], index=year_add_data['2024']['index'])
            df['2025'] = pd.Series(year_add_data['2025']['data'], index=year_add_data['2025']['index'])
            data = df.to_dict()
            year_list.append(2024)
            year_list.append(2025)
        
        # 년도 목록 반복문 돌리기
        for year in year_list :
            year = str(year) # 년도 문자열로 변경
            calc_result = self.year_data_calc(data, year) # 계산 결과 값
            type_result = self.year_type_data_calc(type_code, year) # 업종별 분석 값

            # 해당 년도에 대한 결과 세팅
            result[year] = {
                "계산결과" : calc_result,
                "세무정보" : data[year],
                "동종업계" : type_result
            }
        if jongmok == "null" :
            jongmok = "-"
        result['기업정보'] = {
            "기업명" : name,
            "업종명" : type_name,
            "종목코드" : jongmok,
        }

        return result

    # 업종별 기업들의 재무 정보 계산 결과 값
    def year_type_data_calc(self, type_code, year) :
        # 결과 dict 세팅
        result_list = {
            "매출총이익률" : [],
            "영업이익률" : [],
            "순이익률" : [],
            "매출원가및판관비" : []
        }
        # 변화율 계산용 dict
        trend_result_list = {
            "매출총이익률" : [],
            "영업이익률" : [],
            "순이익률" : [],
            "매출원가및판관비" : []
        }
        
        # 해당하는 업종의 회사 목록 불러오기
        type_list = self.company_type[str(type_code)]
        
        # 해당하는 업종의 회사에 대한 계산 값 구하기
        for name in type_list : 
            # 회사 정보
            type_company = self.company_info[name]

            # 2014, 2024, 2025 년도 데이터 예측 추가 (2015 ~ 2023 데이터가 있는거 한정)
            if len(self.company_year_list(name)) == 9 :
                df = pd.DataFrame(type_company)
                df = df.iloc[:, ~df.columns.isin(['데이터분류', '업종', '업종명', "종목코드"])]
                df = df.fillna(0)
                x_i = list(df.index)
                d_2014 = { "data" : [], "index" : [] }
                d_2024 = { "data" : [], "index" : [] }
                d_2025 = { "data" : [], "index" : [] }
                for x in range(len(x_i)) :
                    d = df.iloc[x, :]
                    x_data = list(map(self.return_arr, list(d.index)))
                    y_data = d.values
                    reg = LinearRegression()
                    reg.fit(x_data, y_data)
                    y_pred = reg.predict([[2014], [2024], [2025]])
                    d_2014['data'].append(int(float(format(y_pred[0], 'f'))))
                    d_2014['index'].append(x_i[x])
                    d_2024['data'].append(int(float(format(y_pred[1], 'f'))))
                    d_2024['index'].append(x_i[x])
                    d_2025['data'].append(int(float(format(y_pred[2], 'f'))))
                    d_2025['index'].append(x_i[x])
                df['2014'] = pd.Series(d_2014['data'], index=d_2014['index'])
                df['2024'] = pd.Series(d_2024['data'], index=d_2024['index'])
                df['2025'] = pd.Series(d_2025['data'], index=d_2025['index'])
                type_company = df.to_dict()

            # 해당하는 년도에 대한 값이 있으면
            if type_company.get(year) : 
                calc_result = self.year_data_calc(type_company, year) # 계산값 구하기
                one_year_calc_result = {} # 직전년도 값 변수 세팅

                # 직전년도 값이 있는지 확인 후 값 세팅
                if type_company.get(str(int(year) - 1)) :
                    one_year_calc_result = self.year_data_calc(type_company, str(int(year) - 1))

                # 평균 구하기
                # 매출총이익률
                if calc_result.get("매출총이익률") :
                    result_list["매출총이익률"].append(calc_result["매출총이익률"])

                # 영업이익률
                if calc_result.get("영업이익률") :
                    result_list["영업이익률"].append(calc_result["영업이익률"])

                # 순이익률
                if calc_result.get("순이익률") :
                    result_list["순이익률"].append(calc_result["순이익률"])

                # 매출 원가 및 판관비 계산용 변수
                wonga = 0
                # 매출원가
                if type_company[year].get("매출원가") : 
                    wonga += type_company[year]["매출원가"]

                # 판관비
                if type_company[year].get("판매비와관리비") :
                    wonga += type_company[year]["판매비와관리비"]

                # 매출원가 + 판관비 있는지 체크
                if type_company[year].get("매출원가") or type_company[year].get("판매비와관리비") : # 매출원가 or 판관비 중 하나라도 잇다면
                    result_list["매출원가및판관비"].append(wonga)
                
                # 변화율 계산
                if not one_year_calc_result == {} :
                    # 매출총이익률 ((당해 매출총이익률 - 직전 매출총이익률) / 직전 매출총이익률 * 100)
                    if calc_result.get("매출총이익률") and one_year_calc_result.get("매출총이익률") :
                        trend_result_list["매출총이익률"].append((calc_result["매출총이익률"] - one_year_calc_result["매출총이익률"]) / one_year_calc_result["매출총이익률"] * 100)

                    # 영업이익률 ((당해 영업이익률 - 직전 영업이익률) / 직전 영업이익률 * 100)
                    if calc_result.get("영업이익률") and one_year_calc_result.get("영업이익률") :
                        trend_result_list["영업이익률"].append((calc_result["영업이익률"] - one_year_calc_result["영업이익률"]) / one_year_calc_result["영업이익률"] * 100)

                    # 순이익률 ((당해 순이익률 - 직전 순이익률) / 직전 순이익률 * 100)
                    if calc_result.get("순이익률") and one_year_calc_result.get("순이익률") :
                        trend_result_list["순이익률"].append((calc_result["순이익률"] - one_year_calc_result["순이익률"]) / one_year_calc_result["순이익률"] * 100)

                    # 매출 원가 및 판관비 계산용 변수
                    last_wonga = 0
                    # 매출원가
                    if type_company.get(str(int(year) - 1)) and type_company[str(int(year) - 1)].get("매출원가") :
                        last_wonga += type_company[str(int(year) - 1)]["매출원가"]

                    # 판관비
                    if type_company.get(str(int(year) - 1)) and type_company[str(int(year) - 1)].get("판매비와관리비") :
                        last_wonga += type_company[str(int(year) - 1)]["판매비와관리비"]

                    # 매출원가 + 판관비 있는지 체크
                    if not wonga == 0 and not last_wonga == 0 : # 둘다 0이 아니면 ((당해 원가 - 직전 원가) / 직전 원가 * 100)
                        trend_result_list["매출원가및판관비"].append((wonga - last_wonga) / last_wonga * 100)

        # 값 세팅
        type_result = {
            "평균" : {}, 
            "중위값" : {},
            "추세" : {}
        }

        if not (result_list["매출총이익률"] == [] or result_list["순이익률"] == [] or result_list["영업이익률"] == [] or result_list["매출원가및판관비"] == []) :
            type_result['평균'] = {
                "매출총이익률" : round(np.mean(result_list["매출총이익률"]), 2),
                "영업이익률" : round(np.mean(result_list["영업이익률"]), 2),
                "순이익률" : round(np.mean(result_list["순이익률"]), 2),
                "매출원가및판관비" : round(np.mean(result_list["매출원가및판관비"])),
            }

            type_result['중위값'] = {
                "매출총이익률" : round(np.median(result_list["매출총이익률"]), 2),
                "영업이익률" : round(np.median(result_list["영업이익률"]), 2),
                "순이익률" : round(np.median(result_list["순이익률"]), 2),
                "매출원가및판관비" : round(np.median(result_list["매출원가및판관비"])),
            }

        # 변화율 항목이 전부 빈 값이 아니면 추세 데이터 생성
        if not (trend_result_list["매출총이익률"] == [] or trend_result_list["순이익률"] == [] or trend_result_list["영업이익률"] == [] or trend_result_list["매출원가및판관비"] == []) :
            type_result["추세"] = {
                "매출총이익률" : round(np.median(trend_result_list["매출총이익률"]), 2),
                "영업이익률" : round(np.median(trend_result_list["영업이익률"]), 2),
                "순이익률" : round(np.median(trend_result_list["순이익률"]), 2),
                "매출원가및판관비변화율" : round(np.median(trend_result_list["매출원가및판관비"])),
            }

        return type_result

    # 각종 비율 계산
    def year_data_calc(self, info, year) : 
        data = info[year] # 해당 년도에 대한 재무 정보 세팅
        calc_result = {} # 결과값 세팅

        # 계산
        # 유동비율 계산 (유동자산 / 유동부채 * 100)
        if data.get("유동자산") and data.get("유동부채") and data["유동부채"] != 0 : 
            calc_result["유동비율"] = round(data["유동자산"] / data["유동부채"] * 100, 2)
        # 부채비율 계산 (부채총계 / 자본총계 * 100)
        if data.get("부채총계") and data.get("자본총계") and data["자본총계"] != 0 :
            calc_result["부채비율"] = round(data["부채총계"] / data["자본총계"] * 100, 2)
        # 자본총계 계산 (자본총계 / 자산총계 * 100)
        if data.get("자본총계") and data.get("자산총계") and data["자산총계"] != 0 : 
            calc_result["자기자본비율"] = round(data["자본총계"] / data["자산총계"] * 100, 2)
        # 매출총이익률 계산 (매출총이익 / 매출액 * 100)
        if data.get("매출총이익") and data.get("매출액") and data["매출액"] != 0 :
            calc_result["매출총이익률"] = round(data["매출총이익"] / data["매출액"] * 100, 2)
        # 영업이익 계산 (영업이익 / 매출액 * 100)
        if data.get("영업이익") and data.get("매출액") and data["매출액"] != 0 :
            calc_result["영업이익률"] = round(data["영업이익"] / data["매출액"] * 100, 2)
        # 순이익률 계산 (순이익 / 매출액 * 100)
        if data.get("순이익") and data.get("매출액") and data["매출액"] != 0 :
            calc_result["순이익률"] = round(data["순이익"] / data["매출액"] * 100, 2)

        return calc_result