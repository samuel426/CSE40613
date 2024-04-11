<?php
    $user_id = $_POST['user_id'];
    $user_pw = $_POST['user_pw'];
    $conn = mysqli_connect('localhost', 'root', 'mysql비번', 'user');
    $sql = "SELECT * FROM member where user_id='$user_id' and user_pw='$user_pw'";
    $res = mysqli_fetch_array(mysqli_query($conn,$sql));
    if($res){
        session_start();
        $_SESSION['user_id'] = $res['user_id'];
        $_SESSION['user_name'] = $res['user_name'];
        echo "<script>alert('Login Success!');";
        echo "window.location.replace('main.php');</script>";
        exit;
    }
    else{
       echo "<script>alert('Wrong ID or PW.');";
       echo "window.location.replace('login.php');</script>";
    }
?>
<meta http-equiv="refresh" content="0;url=main.php">
