<?php
// MySQL 데이터베이스 연결
$servername = "localhost"; // MySQL 서버 주소
$username = "username"; // MySQL 계정 이름
$password = "password"; // MySQL 계정 비밀번호
$dbname = "mydatabase"; // 사용할 데이터베이스 이름

// MySQL 연결 생성
$conn = new mysqli($servername, $username, $password, $dbname);

// 연결 검사
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// POST로부터 사용자가 제출한 username과 password 가져오기
$username = $_POST['username'];
$password = $_POST['password'];

// 입력된 username과 password를 이용하여 데이터베이스에서 검색
$sql = "SELECT * FROM users WHERE username='$username' AND password='$password'";
$result = $conn->query($sql);

// 결과 검사
if ($result->num_rows > 0) {
    // 로그인 성공
    echo "Login successful!";
} else {
    // 로그인 실패
    echo "Login failed. Invalid username or password.";
}

// MySQL 연결 닫기
$conn->close();
?>