import websocket
import socket
import json 
from .config import DEBUG
from .handlers import Cmds, Handlers, decodePacket, encodePacket

if DEBUG:
	websocket.enableTrace(True) 

def doConnect(ws: str, token: str, uid: int, roomId: int, on_receive = None):
	config={
		"token":token,
		"uid":uid,
		"roomId":roomId
	}
	def on_message(wsapp, message):
		"""
		接收消息处理函数
		"""
		print(f"on_message, packet: {message}")
		packet = decodePacket(message)
		cmd = packet["cmd"]
		# 根据cmd获取处理器
		handler = Handlers[cmd]
		if(cmd == Cmds["ROOM_MSG_RECEIVE_S"]):
			handler = on_receive	
		if handler is None:
			print(f"cmd: {cmd}对应的handler不存在")
		handler(packet, wsapp, config)
		
	def on_connect(wsapp):
		"""
		连接事件处理函数
		"""
		print(f"on_open")
		#发起第一个指令
		wsapp.send(encodePacket(Cmds["CONNECT_C"]));
		
	wsapp = websocket.WebSocketApp(ws, on_message=on_message, on_open=on_connect)
	wsapp.run_forever(ping_interval=20, ping_timeout=10, ping_payload="This is an optional ping payload") 

# if __name__ == "__main__":
# 	doConnect()

	