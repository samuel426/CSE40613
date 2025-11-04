# SQL Injection Demo (PHP · MySQL) — 교육용 취약 웹앱

> **목적**: SQL Injection 취약점을 재현하고 공격 PoC와 방어 원칙을 학습하기 위한 데모 프로젝트입니다.  
> **구성**: 로그인/회원가입/메인/관리자/로그아웃 페이지 + 데이터 대량 주입 스크립트 + Blind SQLi 스크립트

---

## 🏗️ 스택 & 구조

- **Backend**: PHP 8.x (Apache + PHP 모듈, 또는 XAMPP/MAMP 등)
- **DB**: MySQL 8.x
- **Scripts**: Python 3.10+ (`requests`, `pandas`, `openpyxl`)

```
project-root/
├─ admin.php        # 관리자 전용 사용자 목록/삭제
├─ join.php         # 회원가입 폼 (POST → join_ok.php)
├─ join_ok.php      # 회원가입 처리 (의도적 취약 쿼리)
├─ login.php        # 로그인 폼 (POST → login_ok.php)
├─ login_ok.php     # 로그인 처리 (의도적 취약 쿼리)
├─ logout.php       # 세션 종료
├─ main.php         # 메인 페이지 (세션 상태에 따라 안내)
├─ random_join.php  # API: 외부에서 다건 사용자 삽입용
├─ random_data.py   # 엑셀 → random_join.php로 대량 주입
└─ bool_sqli.py     # Blind SQL Injection PoC
```

> ⚠️ **중요**: 본 코드는 교육용으로 **의도적으로 취약**하게 작성되어 있습니다. 외부 네트워크에 노출하지 마세요.

---

## 🚀 빠른 시작(Quick Start)

### 1) PHP/Apache/MySQL 설치
- Ubuntu 예시: `sudo apt install apache2 php libapache2-mod-php php-mysqli mysql-server`
- XAMPP 사용 시, `htdocs/YourFolder`에 본 프로젝트 파일들을 넣고 `http://localhost/YourFolder`로 접근

### 2) MySQL 초기화

```sql
-- 1) 데이터베이스 생성
CREATE DATABASE user CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE user;

-- 2) 테이블 생성 (관리 편의를 위해 id 컬럼 포함)
DROP TABLE IF EXISTS member;
CREATE TABLE member (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  user_id   VARCHAR(50) NOT NULL UNIQUE,
  user_name VARCHAR(50) NOT NULL,
  user_pw   VARCHAR(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 3) 초기 관리자 계정
INSERT INTO member (user_id, user_name, user_pw)
VALUES ('admin', 'Admin', 'admin123');
```

> 기존 README의 간단 스키마 대신, 실제 파일들에서 참조하는 `id` 컬럼을 반영해 **AUTO_INCREMENT** 구조로 맞췄습니다.  
> 만약 기존 코드의 `id` 재정렬(UPDATE로 다시 번호 매기기) 부분을 계속 쓰려면 AUTO_INCREMENT 없이 INT 컬럼만 두고 직접 번호를 관리해도 됩니다.

### 3) PHP 코드의 DB 접속정보 수정 (중요)

아래 파일에서 **DB 비밀번호**와 **접속정보**를 여러분 환경에 맞게 통일하세요.

- `login_ok.php`:
  ```php
  $conn = mysqli_connect('localhost', 'root', '여기에_mysql_비번', 'user');
  ```
- `join_ok.php`:
  ```php
  $conn = mysqli_connect('localhost', 'root', '여기에_mysql_비번', 'user');
  ```
- `admin.php`:
  ```php
  $servername = "localhost";
  $username = "root";
  $password = "여기에_mysql_비번";
  $dbname = "user";
  $conn = new mysqli($servername, $username, $password, $dbname);
  ```
- `random_join.php`:
  ```php
  $servername = "localhost";
  $username = "root";
  $password = "여기에_mysql_비번";
  $dbname = "user";
  $conn = mysqli_connect($servername, $username, $password, $dbname);
  ```

> 각 파일의 비밀번호가 서로 다르게 하드코딩돼 있었다면 **모두 같은 값으로 통일**해야 재현/운영이 편합니다.

### 4) 실행

- 배치 경로 예시: `/var/www/html/CSE40613/`
- 브라우저에서 `http://localhost/CSE40613/main.php` 접속
- 초기 로그인: **ID** `admin` / **PW** `admin123`  
- 관리자 페이지: `http://localhost/CSE40613/admin.php` (세션상 admin만 접근)

---

## 🧪 시연 시나리오

1) **회원가입 → 로그인 → 메인**  
   - `join.php` → `join_ok.php` → `login.php` → `login_ok.php` → `main.php`

2) **관리자 페이지(user 목록/삭제)**  
   - `admin.php`에서 전체 사용자 목록 확인 및 삭제 수행

3) **의도적 취약점**  
   - 로그인/가입 처리부에서 사용자 입력을 문자열 결합으로 SQL에 삽입합니다.
   - Blind SQLi 스크립트를 통해 정보 스키마/테이블/컬럼/데이터를 추출하는 과정을 실습합니다.

---

## 📥 데이터 대량 주입 (엑셀 → 서버)

### random_data.py (클라이언트)

```bash
pip install requests pandas openpyxl
```

```python
# random_data.py 내부
excel_file_path = '/절대/또는/상대/경로/MOCK_DATA.xlsx'  # 엑셀 경로
url = 'http://localhost/CSE40613/random_join.php'      # 서버 API 경로
```

- 엑셀 컬럼 예시: `user_id, user_name, user_pw`
- 실행: `python3 random_data.py`

### random_join.php (서버)

- `POST` 로 전달된 `user_id, user_name, user_pw`를 DB에 삽입합니다.
- 에러 로그가 뜨면 `php.ini`의 `display_errors` 설정 또는 Apache 에러 로그(`/var/log/apache2/error.log`)를 확인하세요.

---

## 🕳️ Blind SQL Injection PoC

### bool_sqli.py

```bash
pip install requests pandas
python3 bool_sqli.py
```

- 실행 후 프롬프트에서 **ID 입력**을 요구합니다(공격 시나리오에 따라 사용).
- 스크립트는 `user_id` 파라미터에 Blind SQLi 페이로드를 주입하여
  - DB 개수, 특정 DB명
  - 특정 스키마 내 테이블명
  - 특정 테이블의 컬럼명
  - 행 데이터
  등을 **문자 단위/이진 탐색 방식**으로 추출하도록 구성되어 있습니다.

> 네트워크/보안 정책에 따라 방화벽 혹은 WAF가 차단할 수 있으니 **반드시 로컬 환경**에서만 실습하세요.

---

## 🧯 트러블슈팅

- **Wrong ID or PW**:  
  - DB에 초기 admin 계정이 삽입됐는지, 입력값 오타가 없는지 확인
  - `login_ok.php`의 DB 접속정보(비번/DB명)가 맞는지 확인
- **페이지 이동이 안 됨**:  
  - PHP에서 `session_start()` 호출 여부 확인
  - `<meta http-equiv="refresh">`/`window.location.replace()`가 브라우저에서 동작하는지 확인
- **DB 연결 실패**:  
  - `mysqli_connect`/`new mysqli` 반환값과 `mysqli_error`를 출력해 원인 파악
  - MySQL이 실행 중인지(`systemctl status mysql`)와 계정/권한 확인
- **대량 주입 실패**:  
  - `random_data.py`의 엑셀 경로/시트명, `random_join.php` URL 확인
  - `openpyxl` 미설치 시 설치 필요

---

## 🔐 다음 단계(보안 강화 가이드)

> 교육용 취약 코드를 실제 보안 코드로 전환할 때의 가이드입니다.

1) **Prepared Statement** (PDO 또는 `mysqli_prepare`) 사용  
   ```php
   $stmt = $conn->prepare("SELECT * FROM member WHERE user_id = ? AND user_pw = ?");
   $stmt->bind_param("ss", $user_id, $user_pw);
   $stmt->execute();
   ```
2) **비밀번호 해시** (`password_hash`, `password_verify`) 적용  
3) **에러 메시지 최소화** (내부 로그에만 상세 원인 기록)  
4) **권한 분리** (관리자 페이지/기능을 별도 보호, 최소 권한 DB 계정 사용)  
5) **입력 검증 & 출력 인코딩** (XSS/SQLi/CSRF 등 전반 대응)

---

## 📄 라이선스/주의

- 본 프로젝트는 **교육/연구 목적**으로만 사용하세요.
- 외부 네트워크/공용 서버에 배포하지 마세요.
