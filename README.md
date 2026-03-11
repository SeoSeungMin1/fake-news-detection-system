# AI-based Fake News Detection System

뉴스 기사 URL을 입력하면 해당 뉴스가 가짜 뉴스일 가능성을 예측하는 AI 기반 가짜 뉴스 판별 시스템입니다.  
웹에서 뉴스 기사 본문을 크롤링한 뒤 머신러닝 모델을 통해 분석하고 예측 결과를 반환합니다.

---

# Project Overview

가짜 뉴스로 인한 정보 오염 문제를 해결하기 위해 뉴스 기사 URL을 입력하면 해당 기사의 가짜 뉴스 여부를 예측하는 AI 기반 판별 시스템을 구현했습니다.
입력된 URL로부터 기사 본문을 크롤링한 뒤 머신러닝 모델을 통해 예측을 수행하고 결과를 확률 형태로 제공하여 뉴스의 신뢰도를 정량적으로 확인할 수 있도록 설계했습니다.

---

# Tech Stack

**Language**
- Python

**Machine Learning**
- TF-IDF Vectorizer
- Logistic Regressin
- scikit-learn

**Backend**
- Flask (REST API)

**Data Processing**
- Pandas
- NumPy
 
**Crawling**
- requests
- BeautifulSoup

**Client**
- Android App (Emulator)

---

# System Architecture

뉴스 URL 입력 -> Flask API 서버 -> 뉴스 기사 크롤링 -> TF-IDF 텍스트 벡터화 -> Logistic Regression 모델 예측
-> 예측 결과(JSON) 반환 -> Android App 결과 표시

---

# Key Implementation

- Pandas를 활용하여 True/Fake 뉴스 데이터셋 로드 및 라벨링
- 약 44,898개의 뉴스 기사 데이터셋 구성 및 셔플링
- train_test_split을 통해 학습 80% / 테스트 20% 데이터 분리
- TF-IDF 기반 텍스트 벡터화 (최대 5000개 특징 사용)
- Logistic Regression 기반 가짜 뉴스 분류 모델 학습
- 테스트 데이터 기준 Accuracy 98.81% 달성
- pickle을 이용해 학습된 모델 및 벡터라이저 저장
- Flask 기반 REST API 서버(/predict) 구현
- requests와 BeautifulSoup을 활용한 뉴스 기사 크롤링
- JSON 형태로 예측 결과 반환

---

# Result

- Test Accuracy : **98.81%**
- Android 앱과 서버 간 HTTP 통신을 통해 모바일 환경에서 예측 결과 확인 가능하도록 구현

---

# Limitations

- 한국어 가짜 뉴스 데이터셋 부족으로 인해 **영문 뉴스 데이터셋 사용**
- 가짜 뉴스의 정의가 명확하지 않아 **판별 기준에 한계가 존재**
- 
