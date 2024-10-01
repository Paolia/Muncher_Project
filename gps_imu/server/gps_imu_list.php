<?php

$config = require 'config.php';

$dbn = 'mysql:dbname=tamiok_munch;charset=utf8mb4;port=3306;host=mysql3101.db.sakura.ne.jp';
$user = $config['db_user'];
$pwd = $config['db_password'];

try {
  $pdo = new PDO($dbn, $user, $pwd);
} catch (PDOException $e) {
  echo json_encode(["db error" => "{$e->getMessage()}"]);
  exit();
}

$sql = 'SELECT * FROM gps_imu ORDER BY id ASC';

$stmt = $pdo->prepare($sql);

try {
  $status = $stmt->execute();
} catch (PDOException $e) {
  echo json_encode(["sql error" => "{$e->getMessage()}"]);
  exit();
}

$result = $stmt->fetchAll(PDO::FETCH_ASSOC);
$output = "";
foreach ($result as $record) {
  $output .= "
    <tr>
      <td>{$record["lat"]}</td>
      <td>{$record["lon"]}</td>
      <td>{$record["alt"]}</td>
      <td>{$record["speed"]}</td>
      <td>{$record["gyro_x"]}</td>
      <td>{$record["gyro_y"]}</td>
      <td>{$record["gyro_z"]}</td>
      <td>{$record["accel_x"]}</td>
      <td>{$record["accel_y"]}</td>
      <td>{$record["accel_z"]}</td>
      <td>{$record["temp"]}</td>
    </tr>
  ";
}

?>

<!DOCTYPE html>
<html lang="ja">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>GPS・IMU取得データ</title>
</head>

<body>
  <fieldset>
    <legend>GPS・IMU取得データ一覧</legend>
    <table>
      <thead>
        <tr>
          <th>緯度</th>
          <th>経度</th>
          <th>高度</th>
          <th>速度</th>
          <th>X角加速度</th>
          <th>Y角加速度</th>
          <th>Z角加速度</th>
          <th>X軸加速度</th>
          <th>Y軸加速度</th>
          <th>Z軸加速度</th>
          <th>温度</th>
        </tr>
      </thead>
      <tbody>
        <?= $output ?>
      </tbody>
    </table>
  </fieldset>
</body>

</html>