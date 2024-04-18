<?php
if (!isset($_POST['join_name']) || !isset($_POST['join_id']) || !isset($_POST['join_pw'])) {
    header("Content-type: text/html; charset=UTF-8");
    echo "<script>alert('Fill the blank.')</script>";
    echo "<script>window.location.replace('join.php');</script>";
    exit;
}

$join_id = $_POST['join_id'];
$join_name = $_POST['join_name'];
$join_pw = $_POST['join_pw'];


$conn = mysqli_connect('localhost', 'root', 'mysql비번', 'user');


if (mysqli_connect_errno()) {
    echo "Failed to connect to MySQL: " . mysqli_connect_error();
    exit;
}

$check_query = "SELECT * FROM member WHERE user_id = '$join_id'";
$check_result = mysqli_query($conn, $check_query);

if(mysqli_num_rows($check_result) > 0) {
    echo "<script>alert('Duplicate user ID. Please try another one.');</script>";
    echo "<script>window.location.replace('join.php');</script>";
    exit;
}

$multi = "
        INSERT INTO member(user_id, user_name, user_pw) VALUES ('{$join_id}', '{$join_name}', '{$join_pw}');
        SET @COUNT = 0;
        UPDATE member SET id = @COUNT:=@COUNT+1;
    ";
    $res = mysqli_multi_query($conn,$multi);
    if($res){
        echo "<script>alert('Sign up completed.');";
        echo "window.location.replace('login.php');</script>";
        exit;
    }
    else{
       echo "<script>alert('Something's wrong.');";
       echo mysqli_error($conn);
    }
?>
