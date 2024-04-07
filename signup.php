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

// POST로부터 사용자가 제출한 새로운 username과 password 가져오기
$new_username = $_POST['new_username'];
$new_password = $_POST['new_password'];

// 사용자가 입력한 새로운 username과 password를 데이터베이스에 추가
$sql = "INSERT INTO users (username, password) VALUES ('$new_username', '$new_password')";

if ($conn->query($sql) === TRUE) {
    echo "Sign up successful!";
} else {
    echo "Error: " . $sql . "<br>" . $conn->error;
}

// MySQL 연결 닫기
$conn->close();
?>
