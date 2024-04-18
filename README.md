# 시작하기 앞서

## database를 user로 생성해 주고

```sql
CREATE DATABASE user;
```

## table을 아래와 같이 설정해 주세요

```sql
USE user;

CREATE TABLE member (
    user_id VARCHAR(50) PRIMARY KEY,
    user_name VARCHAR(50),
    user_pw VARCHAR(50)
);
```


## database 비번을 본인의 mysql 비밀번호로 수정해주세요 (mysql 비번 부분)

### join_ok.php, login_ok.php 둘 다 수정하셔야 합니다.

```php
$conn = mysqli_connect('localhost', 'root', 'mysql비번', 'user');
```

## add data in user

```sql
USE user;

INSERT INTO member (user_id, user_name, user_pw) VALUES ('admin', 'Admin', 'admin123');

```
