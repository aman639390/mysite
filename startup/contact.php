<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    mail("your-email@example.com",
         "New Contact Form Message",
         "Name: ".$_POST['name']."\nEmail: ".$_POST['email']."\nMessage: ".$_POST['message']);
}
?>
