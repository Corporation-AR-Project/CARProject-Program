from calculator import Calculator
from data_process import DataProcess
import csv, json, tkinter

# 기업 목록 생성
def company_list() :
    link = entry.get() # 다운로드 파일 위치 가져오기
    dp = DataProcess(link) # Data Process 클래스 생성
    company_list_origin = list(dp.company_info.keys()) # 기업명 가져오기

    # listbox에 기업 목록 생성
    idx = 0 # 인덱스 초기화
    for company in company_list_origin : 
        listbox.insert(idx, company) # listbox에 기업 추가
        idx+=1

# 기업 목록 검색
def company_list_search() : 
    link = entry.get() # 다운로드 파일 위치 가져오기
    keyword = entry2.get() # 검색어 가져오기
    dp = DataProcess(link) # Data Process 클래스 생성
    search_list =  [s for s in list(dp.company_info.keys()) if keyword in s] # 기업 목록에서 검색

    # listbox에 기존에 있었던 값들 제거
    listbox.delete(0, listbox.size() - 1)

    # listbox에 기업 목록 생성
    idx = 0 # 인덱스 초기화
    for company in search_list : 
        listbox.insert(idx, company) # listbox에 기업 추가
        idx += 1

# 결과물 생성
def result_output() :
    link = entry.get() # 다운로드 파일 위치 가져오기
    name = listbox.get(listbox.curselection()[0]) # 선택된 기업명 가져오기
    calc = Calculator(link) # Calculator 클래스 생성
    year_list = calc.company_year_list(name) # 해당 기업의 년도 목록 가져오기
    result = calc.calc(name, year_list) # 결과값 생성

    # company_info.csv 생성 (기업정보 파일)
    with open(link+"/company_info.csv", 'w', encoding='UTF-8', newline='') as file : 
        wr = csv.writer(file)
        wr.writerow(list(result['기업정보'].keys()))
        wr.writerow(list(result['기업정보'].values()))

    # company_analyze.json 생성 (계산 결과값 파일)
    with open(link+'/company_analyze.json','w', encoding='UTF-8') as file :
        json.dump(result, file, indent=4, ensure_ascii=False)

    # JSON 파일 생성 안내 
    text.insert("current", "JSON 파일이 생성되었습니다.")

# tkinter로 GUI 생성  
window = tkinter.Tk()
window.title("기업 매출 분석봇") # 타이틀
window.geometry("450x700+100+100") # 창 크기
window.resizable(False, False) # 창 변형 여부(허용안함)

label=tkinter.Label(window, text="경로 설정", width=10, height=1, fg="black") # 경로 설정 라벨
label.pack()
label.place(x=10, y=32) # 라벨 위치 지정

entry=tkinter.Entry(window, width=47) # 다운로드 경로 입력창
entry.pack()
entry.bind("<Return>", company_list) # Enter 입력시 기업 목록이 나오게 설정
entry.place(x=90, y = 32) # 입력창 위치 지정

label2=tkinter.Label(window, text="기업 검색", width=10, height=1, fg="black") # 기업 검색 라벨
label2.pack()
label2.place(x=10, y=60) # 라벨 위치 지정

entry2=tkinter.Entry(window, width=47) # 기업 검색 입력창
entry2.pack()
entry2.bind("<Return>", company_list_search) # Enter 입력시 검색되도록 설정
entry2.place(x=90, y = 60) # 입력창 위치 지정

listbox = tkinter.Listbox(window, selectmode='single', width=57, height=30) # 기업 목록 Listbox
listbox.yview()
listbox.pack()
listbox.place(x=20,y=90) # listbox 위치 지정

button = tkinter.Button(window, overrelief="solid", width=56, text="검색하기", command=result_output, repeatdelay=1000, repeatinterval=100, bg="black", fg="white") # 검색하기 버튼
button.pack()
button.place(x=20, y=580) # 버튼 위치 지정

text=tkinter.Text(window, width=57, height=5, bg="black", fg="green") # 텍스트 
text.pack()
text.place(x=20, y=620) # 텍스트 위치 지정

window.mainloop() # 윈도우 창 생성
