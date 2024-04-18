<?php
    session_start();
    if (!isset($_SESSION['user_id']) || $_SESSION['user_id'] != 'admin') {
        header("Location: login.php"); // 로그인하지 않았거나 관리자 계정이 아닌 경우 로그인 페이지로 이동
        exit;
    }

    // MySQL 연결
    $servername = "localhost";
    $username = "root"; // MySQL 계정 이름
    $password = "Zz6124042!"; // MySQL 계정 비밀번호
    $dbname = "user"; // 사용할 데이터베이스 이름
    $conn = new mysqli($servername, $username, $password, $dbname);

    // MySQL 연결 검사
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }

    // 삭제 버튼이 클릭된 경우
    if(isset($_POST['delete_user'])) {
        $delete_id = $_POST['delete_user'];
        $delete_query = "DELETE FROM member WHERE user_id='$delete_id'";
        if ($conn->query($delete_query) === TRUE) {
            echo "<script>alert('User deleted successfully');</script>";
        } else {
            echo "<script>alert('Error deleting user: " . $conn->error . "');</script>";
        }
    }

    // 사용자 데이터 가져오기
    $sql = "SELECT * FROM member";
    $result = $conn->query($sql);
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Admin Panel</title>
</head>
<body>
    <h1>Welcome Admin!</h1>
    <p>Here you can manage users and perform administrative tasks.</p>

    <h2>User List:</h2>
    <table>
        <tr>
            <th>User ID</th>
            <th>User Name</th>
            <th>User Password</th>
            <th>Action</th>
        </tr>
        <?php
            if ($result->num_rows > 0) {
                while($row = $result->fetch_assoc()) {
                    echo "<tr>";
                    echo "<td>".$row["user_id"]."</td>";
                    echo "<td>".$row["user_name"]."</td>";
                    echo "<td>".$row["user_pw"]."</td>";
                    // 삭제 버튼 추가
                    echo "<td><form method='post'><button type='submit' name='delete_user' value='".$row["user_id"]."'>Delete</button></form></td>";
                    echo "</tr>";
                }
            } else {
                echo "<tr><td colspan='4'>No users found</td></tr>";
            }
            // MySQL 연결 닫기
            $conn->close();
        ?>
    </table>
</body>
</html>
