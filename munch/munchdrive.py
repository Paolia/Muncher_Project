#! /usr/bin/python3

import RPi.GPIO as GPIO # ラズパイGPIO用標準モジュール
# 東芝TA7291モータコントローラ・ドライバモジュール - モータ用TA7291P、シリンダ用TA7291SGに使用
import ta7291driver 

# 車両のクラス
class MunchDrive():
	# 初期化関数 - ピンと初期速度設定
	def __init__(self):
		self.left = ta7291driver.MotorControl(5,6,12)
		self.right = ta7291driver.MotorControl(19,26,13)
		self.cylinder = ta7291driver.MotorControl(2,3,4)
		# バリカン駆動用に追加（2つ目と3つ目の引数、ピン7&8はダミー）
		self.mower = ta7291driver.MotorControl(4,7,8)
		self.speed = 50
		self.setspeed(self.speed)
		return
	# 速度設定関数
	def setspeed(self, myspeed):
		self.left.setspeed(myspeed)
		self.right.setspeed(myspeed)
		self.speed = myspeed
		return
	# 左超信地旋回関数
	def leftspin(self):
		self.left.accelon()
		self.right.accelon(back=True)
		return
	# 前進左折関数
	def leftturn(self):
		self.left.accelon()
		self.right.acceloff()
		return
	# 後進左折関数
	def revleftturn(self):
		self.left.accelon(back=True)
		self.right.acceloff()
		return
	# 右超信地旋回関数
	def rightspin(self):
		self.left.accelon(back=True)
		self.right.accelon()
		return
	# 前進右折関数
	def rightturn(self):
		self.left.acceloff()
		self.right.accelon()
		return
	# 後進右折関数
	def revrightturn(self):
		self.left.acceloff()
		self.right.accelon(back=True)
		return
	# 前進直進関数
	def forward(self):
		self.left.accelon()
		self.right.accelon()
		return
	# 後進直進関数
	def back(self):
		self.left.accelon(back=True)
		self.right.accelon(back=True)
		return
	# ブレーキ停止関数
	def brake(self):
		self.left.brakeon()
		self.right.brakeon()
		return
	# アクセルオフ減速関数
	def acceloff(self):
		self.left.acceloff()
		self.right.acceloff()
		return
	# シリンダ上昇関数
	def up(self):
		self.cylinder.accelon()
	# シリンダ停止関数
	def hold(self):
		self.cylinder.brakeon()
	# シリンダ下降関数
	def down(self):
		self.cylinder.accelon(back=True)

    # Added
	def mow_on(self):
		self.mower.mowon()
	def mow_off(self):
		self.mower.mowoff()
