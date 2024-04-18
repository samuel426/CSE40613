import pandas as pd
import requests

# # 엑셀 파일 경로
excel_file_path = '/home/sumin/MOCK_DATA.xlsx'

# # 엑셀 파일 읽기
try:
    df = pd.read_excel(excel_file_path)

except Exception as e:
    print(f"엑셀 파일 읽기 오류: {e}")
    exit()

# HTTP POST 요청을 보낼 URL
url = 'http://localhost/CSE40613/random_join.php'


for index, row in df.iterrows():
    user_id = str(row['user_id'])  # 첫 번째 열(user_id)
    user_name = str(row['user_name'])  # 두 번째 열(user_name)
    user_pw = str(row['user_pw'])  # 세 번째 열(user_pw)

    # JSON 데이터 생성
    data = {
        "user_id": user_id,
        "user_name": user_name,
        "user_pw": user_pw
    }


    try:
        # POST 요청 보내기
        response = requests.post(url, data=data)

        # 응답 확인
        if response.status_code == 200:
            print(f"데이터 전송 성공: {data}")
            print(response.text)
        else:
            print(f"데이터 전송 실패: {data}, 응답 코드: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"HTTP 요청 실패: {e}")
