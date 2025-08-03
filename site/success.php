<?php
session_start();

$email = $_SESSION['email'] ?? '';;
$phone = $_SESSION['phone'] ?? '';;
?>

<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Success</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            background-color: #ffffff;
            color: #000;
            margin: 0;
            padding: 20px;
        }
        .container {
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .title {
            font-size: 35px;
            width: 70%;
            font-weight: 900;
            line-height: normal;
            text-transform: uppercase;
            margin-top: 20px;
            margin-bottom: 0px;
        }
        .subtitle {
            margin: 20px auto 20px;
            font-size: 24px;
            font-weight: 700;
            line-height: normal;
        }
        .description {
            margin: 0px auto 20px;
            font-size: 18px;
            font-weight: 700;
            line-height: 140%;
        }

        .small-text {
            font-size: 12px;
            color: #666;
        }
        .info-box {
            background-color: #e7f6e3;
            padding: 25px;
            border-radius: 10px;
            text-align: left;
            margin: 20px 0;
        }
        .info-box h3 {
            text-align: center;
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 10px;
            width: 600px;
        }
        .info-item {
            padding-bottom: 14px;
            margin-bottom: 14px;
            display: flex;
            justify-content: space-between;
            border-bottom: 1px solid rgba(0, 0, 0, 0.5);
            font-size: 14px;
            font-weight: 400;
            line-height: 1;
        }
        </style>
</head>
<body>
    <div class="container">
        <h1 class="title">Thank you very much! Your application is very important to us.</h1>
        <h2 class="subtitle">We have already started processing your application.</h2>
        <p class="description">Our specialist will be in touch with you shortly for more details.</p>

        <p class="small-text">It usually takes no more than 24 hours.</p>

        <div class="info-box">
            <h3>Information about your application</h3>
            <div class="info-item"><span>Email: </span><span><?= htmlspecialchars($email) ?></span></div>
            <div class="info-item"><span>Phone number: </span><span><?= htmlspecialchars($phone) ?></span></div>
            <div class="info-item"><span>Date of submission: </span><span id="current-date"></span></div>
        </div>

    </div>

    </body>
    <script>
        document.addEventListener('DOMContentLoaded', ()=>{
            const date = new Date()
            let currentDate = document.getElementById("current-date")
            currentDate.innerText = `${date.getDate()}.${date.getMonth() + 1}.${date.getFullYear()}`
        })
    </script>
</html>
