# 福岡DEVコース第15期受講者番号13番
# 倉冨民夫 卒業制作

## 内容説明
### 直下階層
  - Substec_Muncher_v4.1.pdf
    企画書

### munchフォルダ
  - ta7291driver.py (Python)
    東芝TA7291シリーズ・モータコントローラのドライバモジュール
  - munchdrive.py (Python)
    上記ドライバモジュールを使用した各モータの動作指示モジュール
  - httpmunch.py (Python)
    Python標準HTTPServerモジュールによるHTTPサーバ機能を利用したWifi遠隔操作プログラム
  - template.html (HTML)
    httpmunch.py操作画面のための表示テンプレート
    mjpg-streamerプログラムによる実機からの動画も表示
  - httpmunch.service (Linuxシェルスクリプト)
    httpmunch.py自動起動スクリプト

### gps_imuフォルダ
  - gps_imu.py (Python)
    GPSおよびIMU（6軸加速度センサ）データ取得・サーバ送信プログラム
  - gps_imu.service (Linuxシェルスクリプト)
    gps_imu.py自動起動スクリプト
 - serverフォルダ
   こちらの内容は次にデプロイ： http://tamiok.sakura.ne.jp
  - write02.php (PHP)
    GPSおよびIMUデータのDB書き込みプログラム
  - config.php (PHP)
    write02.php用データベース設定ファイル（接続情報は除去済）
  - gps_imu_list.php (PHP)
    取得データ一覧表示プログラム
