#! /usr/bin/python3

# /etc/systemd/system/httpmunch.serviceによりデーモン化（自動起動）

# モジュールインポート
from http.server import HTTPServer, BaseHTTPRequestHandler # Python標準HTTPサーバ
from munchdrive import MunchDrive # 車両クラス
from urllib.parse import urlparse # URLクエリ文字列解析

rcmunch = MunchDrive() # 車両クラスのインスタンス

htmltemplate = '<html><head></head><body>Hello,World</body></html>' # htmlテンプレート初期値

# htmlテンプレート読み込み関数
def load_template():
	global htmltemplate
	try:
		f = open('/home/paolia/munch/template.html')
		# ローカル所定の階層のテンプレートファイルを読み込み
	except:
		return
	    # 読み込めない場合は初期値
	htmltemplate = f.read()
	f.close()
	return

# HTTPリクエストハンドラ・クラス
class HelloHandler(BaseHTTPRequestHandler):
	# クエリ解析
	def parse_query(self):
		query = urlparse(self.path).query
		querylist = query.split("&")
		query_components = {}
		
		for item in querylist:
			q = item.split("=")
			if len(q) == 2:
				query_components[q[0]] = q[1]
		return query_components
	
	# 操作設定関数呼び出し
	def action_munch(self,qc):
		global rcmunch
		if 'cmd' in qc:
			cmd = qc['cmd']
			if cmd == 'FWD':
				rcmunch.forward()
			elif cmd == 'FWD_LEFT':
				rcmunch.leftturn()
			elif cmd == 'FWD_RIGHT':
				rcmunch.rightturn()
			elif cmd == 'REV':
				rcmunch.back()
			elif cmd == 'REV_LEFT':
				rcmunch.revleftturn()
			elif cmd == 'REV_RIGHT':
				rcmunch.revrightturn()
			elif cmd == 'SPIN_LEFT':
				rcmunch.leftspin()
			elif cmd == 'SPIN_RIGHT':
				rcmunch.rightspin()
			elif cmd == 'brake':
				rcmunch.brake()
			elif cmd == 'acceloff':
				rcmunch.acceloff()
			elif cmd == 'UP':
				rcmunch.up()
			elif cmd == 'HOLD':
				rcmunch.hold()
			elif cmd == 'DOWN':
				rcmunch.down()
			elif cmd == 'mowon':
				rcmunch.mow_on()
			elif cmd == 'mowoff':
				rcmunch.mow_off()
		if 'speed' in qc:
			try:
				sp = int(qc['speed'])
			except:
				return -1
			if sp >= 50 and sp <= 100 and sp != rcmunch.speed:
				rcmunch.setspeed(sp)
		return 0
	
	# HTML設定関数
	def gen_html(self,qc):
		global htmltemplate
		global rcmunch
		html = htmltemplate
		html = html.replace('__SPEED__',str(rcmunch.speed))
		chtag = "__"+str(rcmunch.speed)+"__"
		html = html.replace(chtag, "checked")
		for s in range(50,110,10):
			s = '__'+str(s)+'__'
			html = html.replace(s,'')
		return html
	
    # 応答関数
	def do_GET(self):
		self.send_response(200)
		self.send_header('Content-type', 'text/html; charset=utf-8')
		self.end_headers()
		
		qc = self.parse_query()
		self.action_munch(qc)
		html = self.gen_html(qc)
		self.wfile.write(html.encode())

# メイン関数
if __name__ == '__main__':
	load_template() # テンプレート読み込み
	server_address = ('', 8000) # サーバポート設定
	httpd = HTTPServer(server_address, HelloHandler) # サーバ設定（アドレス、イベントハンドラ）
	httpd.serve_forever() # サーバ実行