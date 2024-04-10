<!DOCTYPE html>
<?php session_start(); ?>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Main</title>
</head>
<body>
    <h1>MAIN</h1>
    <?php
        if(!isset($_SESSION['user_id']) || !isset($_SESSION['user_name'])) {
            echo "<p>Please Sign in.</p>";
            echo "<p><button onclick=\"window.location.href='login.php'\">Sign in</button> <button onclick=\"window.location.href='join.php'\">Sign up</button></p>";
        } else {
            $user_id = $_SESSION['user_id'];
            $user_name = $_SESSION['user_name'];
            echo "<p>Welcome $user_name($user_id)";
            echo "<p><button onclick=\"window.location.href='logout.php'\">Logout</button></p>";
        }
    ?>
</body>
</html>
