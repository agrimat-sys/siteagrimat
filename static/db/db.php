<?php
$host='localhost'; $db='obripesada_ri'; $user='root'; $pass='';
try{
    $pdo=new PDO("mysql:host=$host;dbname=$db;charset=utf8mb4",$user,$pass,
                 [PDO::ATTR_ERRMODE=>PDO::ERRMODE_EXCEPTION]);
}catch(PDOException $e){
    die("DB error: ".$e->getMessage());
}
?>
