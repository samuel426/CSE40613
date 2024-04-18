<?php
    // check error log
    error_reporting(E_ALL);
    ini_set('display_errors', '1');
    var_dump($_POST);
    // POST 요청이 왔는지 확인
    if (isset($_POST['user_id'])) {
        echo "<script>console.log('post ok');</script>";
        // POST로 전송된 데이터 추출
        $user_id = $_POST['user_id'];
        $user_name = $_POST['user_name'];
        $user_pw = $_POST['user_pw'];

        // MySQL 데이터베이스 연결 설정
        $servername = "localhost";
        $username = "root";
        $password = "3711mm@@";
        $dbname = "user";

        // MySQL 데이터베이스 연결
        $conn = new mysqli($servername, $username, $password, $dbname);

        // 연결 확인
        if ($conn->connect_error) {
            die("MySQL 연결 실패: " . $conn->connect_error);
        }

        // 사용자 정보 삽입 쿼리 실행
        $check_query = "SELECT * FROM member WHERE user_id = '$user_id'";
        $check_result = mysqli_query($conn, $check_query);

        if(mysqli_num_rows($check_result) > 0) {
            echo "<script>console.log('이미 존재하는 아이디입니다');</script>";
        exit;
        }

        $multi = "INSERT INTO member (user_id, user_name, user_pw) VALUES ('{$user_id}', '{$user_name}', '{$user_pw}')";
        $res = mysqli_query($conn, $multi);
        if($res){
            echo "<script>console.log('새로운 레코드가 성공적으로 삽입되었습니다.');</script>";
            exit;
        }
        else{
        echo "<script>Something's wrong.</script>";
        echo mysqli_error($conn);
        }
    }else{
        echo "<script>console.log('not post');</script>";
    }

?>