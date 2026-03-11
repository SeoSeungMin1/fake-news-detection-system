import flask
from flask import Flask, request, jsonify
import pickle
import numpy as np
import requests
from bs4 import BeautifulSoup
import os

# --- 1. 파일 경로 지정 ---
MODEL_PATH = 'logistic_model.pkl'
VECTORIZER_PATH = 'tfidf_vectorizer.pkl'

try:
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    
    with open(VECTORIZER_PATH, 'rb') as f:
        vectorizer = pickle.load(f)
    
    print("✅ 모델 및 벡터라이저 로드 완료. 서버 준비 완료.")
    
except FileNotFoundError:
    print("❌ 오류: 모델 파일(.pkl)을 app.py와 같은 폴더에 넣어주세요!")
    exit()

app = Flask(__name__)

# 웹 크롤링 시 브라우저인 것처럼 위장하기 위한 헤더 설정
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "Invalid input format."}), 400

    news_text_content = ""
    
    if 'url' in data:
        # URL 입력 시: 웹 크롤링 수행
        url = data['url']
        try:
            # User-Agent 헤더를 포함하여 요청
            response = requests.get(url, headers=HEADERS, timeout=10) 
            response.raise_for_status() # HTTP 오류 시 예외 발생
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 기사 본문으로 추정되는 모든 <p> 태그의 텍스트를 합침
            paragraphs = soup.find_all('p')
            news_text_content = ' '.join([p.get_text() for p in paragraphs])
            
            if len(news_text_content) < 100:
                # 텍스트 추출 부족 시: 대체 로직 (제목 + 페이지 상단 1000자)
                title = soup.find('title').get_text() if soup.find('title') else ""
                news_text_content = title + " " + soup.get_text()[:1000] 
                
        except requests.exceptions.RequestException as e:
            # 크롤링 요청 오류 시 400 Bad Request 반환 (500 오류 방지)
            return jsonify({"error": f"URL 요청 또는 크롤링 오류: 주소를 확인하세요. ({e})"}), 400
        
    elif 'text' in data:
        # 텍스트 직접 입력 시: 기존 로직
        news_text_content = data['text']
    
    else:
        return jsonify({"error": "유효한 'url' 또는 'text' 필드가 요청에 필요합니다."}), 400

    # 3. 모델 예측 시작
    if not news_text_content or len(news_text_content.strip()) < 50:
        return jsonify({"error": "기사 내용을 추출하지 못했거나 내용이 너무 짧습니다. (최소 50자 필요)"}), 400
        
    text_for_model = [news_text_content] 
    text_vectorized = vectorizer.transform(text_for_model)

    probabilities = model.predict_proba(text_vectorized)[0]
    fake_probability = probabilities[1]
    
    response = {
        "is_fake_probability": round(fake_probability * 100, 2),
        "is_real_probability": round(probabilities[0] * 100, 2),
        "prediction_label": int(np.argmax(probabilities)),
        "extracted_text_length": len(news_text_content) 
    }
    
    return jsonify(response)

# --- 4. 서버 실행 ---
if __name__ == '__main__':
    print("📢 서버 실행 중. http://127.0.0.1:5000/predict 로 POST 요청을 보내세요.")
    # 포트 5000으로 서버 실행
    app.run(debug=True, port=5000)