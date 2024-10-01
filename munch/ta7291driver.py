#! /usr/bin/python3
import RPi.GPIO as GPIO # ラズパイGPIO用標準モジュール
from time import sleep # sleepで待機の為←未使用、ブレーキで使用か？

# 走行状況パラメータ
ST_STOP = 0
ST_ON = 1

# モータ制御のクラス
class MotorControl :
	# 初期設定関数 - ピン設定など
	def __init__(self,pina,pinb,pwmpin):
		self.state = ST_STOP
		self.pina = pina
		self.pinb = pinb
		self.pwmpin = pwmpin
		self.duty = 0

		# 周波数変更
		# self.pulse = 1000
		# self.pulse = 200

		GPIO.setmode(GPIO.BCM)
		
		GPIO.setup(self.pina, GPIO.OUT)
		GPIO.output(self.pina, GPIO.LOW)
		
		GPIO.setup(self.pinb, GPIO.OUT)
		GPIO.output(self.pinb, GPIO.LOW)
		
		GPIO.setup(self.pwmpin, GPIO.OUT)
		GPIO.output(self.pwmpin, GPIO.LOW)
		
		# 周波数変更
		# self.pwm = GPIO.PWM(self.pwmpin,1000)
		self.pwm = GPIO.PWM(self.pwmpin,30)
		return

	# デューティ比による速度設定関数 
	def setspeed(self,duty):
		self.duty = duty
		if self.state == ST_ON:
			self.pwm.ChangeDutyCycle(self.duty)
		return self.state
	
	# 加速関数
	def accelon(self, back = False):
		if back == False:
			GPIO.output(self.pina, GPIO.HIGH)
			GPIO.output(self.pinb, GPIO.LOW)
		else:
			GPIO.output(self.pina, GPIO.LOW)
			GPIO.output(self.pinb, GPIO.HIGH)
		if self.state == ST_STOP:
			self.pwm.start(self.duty)
		self.state = ST_ON
		return self.state
	
	# 減速関数 - PinAとPinBをLOWにして抵抗により減速
	def acceloff(self):
		GPIO.output(self.pina, GPIO.LOW)
		GPIO.output(self.pinb, GPIO.LOW)
		self.pwm.stop()
		self.state = ST_STOP
		return self.state
	
	# ブレーキ関数 - 一瞬PinAとPinBをHIGHにして強制的に停止する
	def brakeon(self):
		GPIO.output(self.pina, GPIO.HIGH)
		GPIO.output(self.pinb, GPIO.HIGH)
		self.pwm.stop()
		GPIO.output(self.pina, GPIO.LOW)
		GPIO.output(self.pinb, GPIO.LOW)
		self.state = ST_STOP
		return self.state
	
	def mowon(self):
		GPIO.output(self.pina, GPIO.HIGH)
	def mowoff(self):
		GPIO.output(self.pina, GPIO.LOW)