import requests
import json

# ----------------------------------------------------------------------
# ⚠️ 주의: 테스트할 가짜 또는 진짜 뉴스의 URL을 여기에 입력하세요.
# 데이터셋에 사용된 영문 기사 URL을 테스트하는 것이 가장 좋습니다.
# ----------------------------------------------------------------------
TEST_URL = "https://edition.cnn.com/2025/10/14/africa/madagascar-president-dissolves-national-assembly-intl" 

# Flask 서버의 주소 (로컬에서 실행 중이므로)
API_ENDPOINT = "http://127.0.0.1:5000/predict"

# 서버로 보낼 데이터 (URL을 담아 보냅니다)
payload = {
    "url": TEST_URL
}

print(f"✅ URL: {TEST_URL} 분석 요청 중...")

try:
    # POST 요청 보내기
    response = requests.post(API_ENDPOINT, json=payload)
    response.raise_for_status() # HTTP 오류 시 예외 처리

    # JSON 응답 받기
    result = response.json()

    print("\n--- 분석 결과 ---")
    if 'error' in result:
        print(f"❌ 오류 발생: {result['error']}")
    else:
        fake_prob = result.get('is_fake_probability', 'N/A')
        prediction = "가짜 (FAKE)" if result.get('prediction_label') == 1 else "진짜 (REAL)"
        extracted_len = result.get('extracted_text_length', 0)

        print(f"👍 분석 성공 (추출된 텍스트 길이: {extracted_len}자)")
        print(f"👉 가짜일 확률: {fake_prob}%")
        print(f"👉 최종 판별: {prediction}")
        print("\n(이 확률을 Android 앱에 표시하게 됩니다.)")

except requests.exceptions.RequestException as e:
    print(f"\n❌ 서버 통신 오류가 발생했습니다. 서버가 실행 중인지 확인하세요.")
    print(f"오류 상세: {e}")