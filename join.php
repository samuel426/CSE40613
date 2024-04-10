<!DOCTYPE html>
<?php session_start(); ?>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Join</title>
    </head>
    <body>
        <h2>Sign up</h2>
        <?php if(!isset($_SESSION['user_id']) || !isset($_SESSION['user_name'])) { ?>
        <form method="post" action="join_ok.php" autocomplete="off">
            <p>name: <input type="text" name="join_name" required></p>
            <p>ID: <input type="text" name="join_id" required></p>
            <p>PW: <input type="password" name="join_pw" required></p>
            <p><input type="submit" value="Submit"></p>
        </form>
        <small><a href="login.php">Already have an account?</a><small>
        <?php } else {
                $user_id = $_SESSION['user_id'];
                $user_name = $_SESSION['user_name'];
                echo "<p>$user_name($user_id), already signed in.";
                echo "<p><button onclick=\"window.location.href='main.php'\">Back Home</button> <button onclick=\"window.location.href='logout.php'\">Logout</button></p>";
        } ?>
    </body>
</html>
