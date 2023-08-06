
import json


Cmds={
    "CONNECT_C": 100,
    "CONNECT_S": 101,
    "LOGIN_C": 102,
    "LOGIN_S": 103,
    "ENTER_ROOM_C": 104,
    "ENTER_ROOM_S": 105,
    "ROOM_MSG_SEND_C": 106,
    "ROOM_MSG_RECEIVE_S": 107
}

def encodePacket(cmd: int, data = None):
	"""
	报文编码
	"""
	packet={"cmd": cmd}
	if data:
		packet["data"] = data
	return json.dumps(packet, indent = 4) 

def decodePacket(jsonData: str):
	"""
	报文解码
	"""
	packet= json.loads(jsonData)
	return packet 

def connect_handler(packet: dict, client, config):
    """
	connnect_s处理函数
	"""
    print(f"connect handler")
    sendPacket = encodePacket(Cmds["LOGIN_C"], data={"token": config["token"]})                
    client.send(sendPacket)
    
def login_handler(packet: dict, client, config):
    """
	login_s处理函数
	"""
    print(f"login handler")
    sendPacket = encodePacket(Cmds["ENTER_ROOM_C"], data={"roomId": config["roomId"]})                
    client.send(sendPacket)
    
def room_enter_handler(packet: dict, client, config):
	"""
	room_enter_s处理函数
	"""
	print(f"room enter handler")
	if packet["data"]["roomId"] is None:
		print(f"[ERROR]房间登录失败")
	
def msg_receive_handler(packet: dict, client, config):
	"""
	房间消息接收处理器
	"""
	print(f"收到房间消息:{packet}")

Handlers={
    Cmds["CONNECT_S"]: connect_handler,
    Cmds["LOGIN_S"]: login_handler,
    Cmds["ENTER_ROOM_S"]: room_enter_handler,
    Cmds["ROOM_MSG_RECEIVE_S"]: msg_receive_handler 
}


    