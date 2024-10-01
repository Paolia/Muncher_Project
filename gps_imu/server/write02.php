<?php

// 08_php03_sample/todo_create.php
if (
  !isset($_POST['lat']) || $_POST['lat'] === '' ||
  !isset($_POST['lon']) || $_POST['lon'] === '' ||
  !isset($_POST['alt']) || $_POST['alt'] === '' ||
  !isset($_POST['speed']) || $_POST['speed'] === '' ||
  !isset($_POST['temp']) || $_POST['temp'] === '' ||
  !isset($_POST['gyro_x']) || $_POST['gyro_x'] === '' ||
  !isset($_POST['gyro_y']) || $_POST['gyro_y'] === '' ||
  !isset($_POST['gyro_z']) || $_POST['gyro_z'] === '' ||
  !isset($_POST['accel_x']) || $_POST['accel_x'] === '' ||
  !isset($_POST['accel_y']) || $_POST['accel_y'] === '' ||
  !isset($_POST['accel_z']) || $_POST['accel_z'] === ''
) {
  exit('paramError');
}

$lat = $_POST['lat'];
$lon = $_POST['lon'];
$alt = $_POST['alt'];
$speed = $_POST['speed'];
$temp = $_POST['temp'];
$gyro_x = $_POST['gyro_x'];
$gyro_y = $_POST['gyro_y'];
$gyro_z = $_POST['gyro_z'];
$accel_x = $_POST['accel_x'];
$accel_y = $_POST['accel_y'];
$accel_z = $_POST['accel_z'];

// DB接続
$config = require 'config.php';

// $dbn = 'mysql:dbname=mun_gps;charset=utf8mb4;port=3306;host=localhost';
$dbn = 'mysql:dbname=tamiok_munch;charset=utf8mb4;port=3306;host=mysql3101.db.sakura.ne.jp';
$user = $config['db_user'];
$pwd = $config['db_password'];

try {
  $pdo = new PDO($dbn, $user, $pwd);
} catch (PDOException $e) {
  echo json_encode(["db error" => "{$e->getMessage()}"]);
}

// DB接続
$dbn = 'mysql:dbname=tamiok_munch;charset=utf8mb4;port=3306;host=mysql3101.db.sakura.ne.jp';
$user = 'tamiok_munch';
$pwd = 'Munch2233';

try {
  $pdo = new PDO($dbn, $user, $pwd);
} catch (PDOException $e) {
  echo json_encode(["db error" => "{$e->getMessage()}"]);
  exit();
}

$sql = 'INSERT INTO gps_imu(id, lat, lon, alt, speed, gyro_x, gyro_y, gyro_z, accel_x, accel_y, accel_z, temp, timest) VALUES(NULL, :lat, :lon, :alt, :speed, :gyro_x, :gyro_y, :gyro_z, :accel_x, :accel_y, :accel_z, :temp, now())';

$stmt = $pdo->prepare($sql);
$stmt->bindValue(':lat', $lat, PDO::PARAM_STR);
$stmt->bindValue(':lon', $lon, PDO::PARAM_STR);
$stmt->bindValue(':alt', $alt, PDO::PARAM_STR);
$stmt->bindValue(':speed', $speed, PDO::PARAM_STR);
$stmt->bindValue(':temp', $temp, PDO::PARAM_STR);
$stmt->bindValue(':gyro_x', $gyro_x, PDO::PARAM_STR);
$stmt->bindValue(':gyro_y', $gyro_y, PDO::PARAM_STR);
$stmt->bindValue(':gyro_z', $gyro_z, PDO::PARAM_STR);
$stmt->bindValue(':accel_x', $accel_x, PDO::PARAM_STR);
$stmt->bindValue(':accel_y', $accel_y, PDO::PARAM_STR);
$stmt->bindValue(':accel_z', $accel_z, PDO::PARAM_STR);

try {
  $status = $stmt->execute();
} catch (PDOException $e) {
  echo json_encode(["sql error" => "{$e->getMessage()}"]);
  exit();
}

// header("Location:input02.php");
exit();
