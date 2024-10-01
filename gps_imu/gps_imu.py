#!/usr/bin/python

# /etc/systemd/system/gps_imu.serviceによりデーモン化（自動起動）

# 共通
import requests # DBへデータを送付するためのRequestsモジュール
from time import sleep # timeモジュール
# GPS用
from gps3 import gps3
# IMU（ジャイロ）用
import smbus # to use I2C
import math
# GPSはUART、IMUはI2Cバスにて通信

# DBへ書き込むPHPのURL
URL = 'http://tamiok.sakura.ne.jp/write02.php'

# GPS向け設定
gps_socket = gps3.GPSDSocket()
data_stream = gps3.DataStream()
gps_socket.connect()
gps_socket.watch()

# DBへデータをアップロード（POST）する関数
def send_to_server(data):
    try:
        response = requests.post(URL, data=data)
        print(f'Sent data: {data}, Server response: {response.text}')
    except Exception as e:
        print(f'Error sending data: {e}')


# IMU関係関数
# 各種パラメータ設定
imu_addr = 0x68   # IMUのアドレス
pwr_mgmt_1 = 0x6b # パワーマネジメント 1
accel_X_out = 0x3b # X軸加速度
accel_Y_out = 0x3d # Y軸加速度
accel_Z_out = 0x3f # Z軸加速度
temp_out = 0x41   # 温度
gyro_X_out = 0x43  # X軸角速度
gyro_Y_out = 0x45  # Y軸角速度
gyro_Z_out = 0x47  # Z軸角速度
 
# 1バイト読み取り
def read_byte(addr):
    return bus.read_byte_data(imu_addr, addr)
 
# ２バイト読み取り
def read_word(addr):
    high = read_byte(addr)
    low  = read_byte(addr+1)
    return (high << 8) + low
 
# IMUセンサデータ読み取り
def read_word_sensor(addr):
    val = read_word(addr)
    if(val < 0x8000):
        return val # 正の値
    else:
        return val - 65536 # 負の値
 
# 温度取得
def get_temp():
    temp = read_word_sensor(temp_out)
    # オフセット値 = -521 @ 35℃
    return (temp + 521) / 340.0 + 35.0
 
# 角速度データ取得（Raw値）
def get_gyro_data_lsb():
    x = read_word_sensor(gyro_X_out)
    y = read_word_sensor(gyro_Y_out)
    z = read_word_sensor(gyro_Z_out)
    return [x, y, z]

# 角速度データ整形（度／秒）－ Raw値を感度値で調整
def get_gyro_data_deg():
    x,y,z = get_gyro_data_lsb()
    # 感度 = 131 LSB（Least Significan Bit）/（度／秒）、データシートより
    x = x / 131.0
    y = y / 131.0
    z = z / 131.0
    return [x, y, z]
 
# 加速度データ取得（Raw値）
def get_accel_data_lsb():
    x = read_word_sensor(accel_X_out)
    y = read_word_sensor(accel_Y_out)
    z = read_word_sensor(accel_Z_out)
    return [x, y, z]

# 加速度データ整形　（G値）－ Raw値を感度値で調整
def get_accel_data_g():
    x,y,z = get_accel_data_lsb()
    # 感度 = 16384 LSB/（G）、データシートより
    x = x / 16384.0
    y = y / 16384.0
    z = z / 16384.0
    return [x, y, z]
# IMU関係関数ここまで


# GPSセンサのためにI2Cバスを準備
bus = smbus.SMBus(1)
bus.write_byte_data(imu_addr, pwr_mgmt_1, 0) 

# GPSデータを取り出し、それにIMUのデータを挿入
for new_data in gps_socket:
  if new_data:
    # GPSデータをアンパック
    data_stream.unpack(new_data)
    timest = data_stream.TPV['time']
    lat = data_stream.TPV['lat']
    lon = data_stream.TPV['lon']
    alt = data_stream.TPV['alt']
    speed =  data_stream.TPV['speed']
    # IMUデータを挿入
    temp = get_temp()
    gyro_x,gyro_y,gyro_z = get_gyro_data_deg()
    accel_x,accel_y,accel_z = get_accel_data_g()

    # DBへ送信するデータをJSON形式で作成
    senddata = {
                'timest': timest,
                'lat': lat,
                'lon': lon,
                'alt': alt,
                'speed': speed,
                'temp': temp,
                'gyro_x':gyro_x,
                'gyro_y':gyro_y,
                'gyro_z':gyro_z,
                'accel_x':accel_x,
                'accel_y':accel_y,
                'accel_z':accel_z
            }
    
    if lat != 'n/a': # GPSのデータがあるときは
        send_to_server(senddata) # DBにデータを送る
    sleep(1) # １秒待機
