<?php
echo "PHP работает<br>";
$data = [
   'first_name' => $_POST['first_name'],
   'last_name' => $_POST['last_name'],
   'email' => $_POST['email'], 
   'phone' => $_POST['phone_number'], 
   'ip' =>  $_SERVER['REMOTE_ADDR'],
   'landing_url' => 'MTF',
];

$payload = json_encode($data);
$API_KEY = "ba67df6a-a17c-476f-8e95-bcdb75ed3958"; 

if ($payload === false) {
    die('Ошибка JSON: ' . json_last_error_msg());
}

$curl = curl_init();
curl_setopt_array($curl, [
    CURLOPT_URL => "http://127.0.0.1:8000/leads/",
    CURLOPT_HTTPHEADER => [
        'Content-Type: application/json',
        "X-API-Key: $API_KEY",
                            ],
    CURLOPT_POST => true,
    CURLOPT_POSTFIELDS => $payload,
    CURLOPT_RETURNTRANSFER => true,
]);

$response = curl_exec($curl);
if ($response === false) {
    echo 'Ошибка cURL: ' . curl_error($curl);
} else {
    echo 'Ответ FastAPI: ' . $response;
}
curl_close($curl);



session_start();

$_SESSION['email'] = $_POST['email'];
$_SESSION['phone'] = $_POST['phone_number'];

header("Location: success.php");

?>
