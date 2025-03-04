from calculator import Calculator
from data_process import DataProcess
import csv, json, tkinter

def company_list(event) :
    link = entry.get()
    dp = DataProcess(link)
    company_list_origin = list(dp.company_info.keys())
    idx = 0
    for company in company_list_origin : 
        listbox.insert(idx, company)
        idx+=1

def company_list_search(event) : 
    link = entry.get()
    keyword = entry2.get()
    dp = DataProcess(link)
    search_list =  [s for s in list(dp.company_info.keys()) if keyword in s] 
    idx = 0

    listbox.delete(0, listbox.size() - 1)

    for company in search_list : 
        listbox.insert(idx, company)
        idx += 1

def return_arr(data) :
    return [data]

def result_output() :
    link = entry.get()
    name = listbox.get(listbox.curselection()[0])
    calc = Calculator(link)
    year_list = calc.company_year_list(name)
    result = calc.calc(name, year_list)
    with open(link+"/company_info.csv", 'w', encoding='UTF-8', newline='') as file : 
        wr = csv.writer(file)
        wr.writerow(list(result['기업정보'].keys()))
        wr.writerow(list(result['기업정보'].values()))
    with open(link+'/company_analyze.json','w', encoding='UTF-8') as file :
        json.dump(result, file, indent=4, ensure_ascii=False)
    text.insert("current", "JSON 파일이 생성되었습니다.")


window = tkinter.Tk()
window.title("기업 매출 분석봇")
window.geometry("450x700+100+100")
window.resizable(False, False)

label=tkinter.Label(window, text="경로 설정", width=10, height=1, fg="black")
label.pack()
label.place(x=10, y=32)

entry=tkinter.Entry(window, width=47)
entry.pack()
entry.bind("<Return>", company_list)
entry.place(x=90, y = 32)

label2=tkinter.Label(window, text="기업 검색", width=10, height=1, fg="black")
label2.pack()
label2.place(x=10, y=60)

entry2=tkinter.Entry(window, width=47)
entry2.pack()
entry2.bind("<Return>", company_list_search)
entry2.place(x=90, y = 60)

listbox = tkinter.Listbox(window, selectmode='single', width=57, height=30)
listbox.yview()
listbox.pack()
listbox.place(x=20,y=90)

button = tkinter.Button(window, overrelief="solid", width=56, text="검색하기", command=result_output, repeatdelay=1000, repeatinterval=100, bg="black", fg="white")
button.pack()
button.place(x=20, y=580)

text=tkinter.Text(window, width=57, height=5, bg="black", fg="green")
text.pack()
text.place(x=20, y=620)

window.mainloop()
