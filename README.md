# CARProject-Program (Corporate Analysis Report - Program)
글로벌 아카데미 차세대 AI 예측 Solution 개발(Java, Python) (5회차) - 1조 프로젝트 : 기업분석리포트 프로젝트 프로그램

## 📌 프로젝트 소개
기업분석리포트 프로젝트는 [전자공시시스템](https://dart.fss.or.kr/main.do)(DART : Data Analysis, Retrieval and Transfer System)의 정보를 활용하여 기업의 재무정보를 분석 및 예측하여 누구나 쉽게 파악할 수 있는 보고서를 제공하는 사이트를 제작하는 것을 목표로 하고 있습니다.

해당 repository 에서는 미니 프로젝트의 프로그램 부분을 관리하고 있습니다.

## 📅 개발 기간
+ 총 기간 : 2025/02/03 ~ 2025/03/07 
    + 기획 및 시스템 설계 : 2025/02/03 ~ 2025/02/06 ✅
    + 데이터 분석 및 정제 : 2025/02/07 ~ 2025/02/28 ✅
    + 설계 및 구현 : 2025/02/07 ~ 2025/03/05 ✅
    + 프로젝트 테스트 : 2025/03/05 ~ 2025/03/07 ✅

## 👤 팀 구성
|이름|역할|
|---|--------|
|연지수|(팀장) 기획 및 시스템 설계, Back-end 설계 및 구현|
|김진영|데이터 분석 및 정제, Back-end 구현|
|박수연|Front-end 설계 및 구현|
|장하은|데이터 분석 및 정제, Back-end 구현|
|최현진|데이터 분석, 발표 자료 제작|

## 개발 환경
+ `python 3.12.8`
+ `tkinter`

## 실행방법
CARProject-Program의 실행방법에 대해 기술합니다.

### Install 
실행 전, 아래 패키지를 Install 합니다.
``` py
# numpy
pip install numpy

# pandas
pip install pandas

# pyinstaller
pip install pyinstaller

# sklearn
pip install -U scikit-learn
```

### Build

프로그램 실행 파일을 Build 합니다.
```
pyinstaller --add-data "calculator.py;data_process.py" --add-data "json/*;json" -w -F project.py
```