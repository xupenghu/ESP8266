import network
import socket     #网络套接字和python一样
from machine import Pin,PWM
import time

UDP_server_addr = ('115.28.93.201', 7005)  #115.28.93.201 端口：UDP 7005
SSID = your_wifi_ssid	#路由器名称
PASSWORD = your_wifi_password	#路由器密码
wlan = network.WLAN(network.STA_IF)

UserID = your_user_ID
DeviceID = your_device_id
MM = your_mm	#16位密码


servo1 = PWM(Pin(12), freq = 50)
servo1.duty(130)
servo2 = PWM(Pin(14), freq = 50)
servo2.duty(130)
time.sleep(2)
servo1.deinit()
servo2.deinit()

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  #生成新的套接字对象
Heart = r"004532A01" + DeviceID + MM +  r"123401hi05" #心跳包

# 连接网络
def do_connect():
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(SSID, PASSWORD)
    start = time.time()
    while not wlan.isconnected():
        time.sleep(1)
        if time.time()-start > 5:
            print("connect timeout!")
            break
	#如果连接成功
    if wlan.isconnected():
	    print('network connect success . \nnetwork config:', wlan.ifconfig())
			
def shakeHand_UDP_server():    
    global client    
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  #生成新的套接字对象
    client.settimeout(5)  #设置连接超时时间    
    while True:        
        print("sendto: " + Heart)
        len = client.sendto(Heart, UDP_server_addr)  #向服务器发送心跳包 
        print("sendlen : " + str(len) )
        time.sleep(0.5)
        try:
            print("now recv...")
            data, addr = client.recvfrom(64)  #接收心跳包数据
            print(b"recv :" + data)
            break
        except:
            print("recv error!")
        time.sleep(10)
			
def revMsgAndKeepConnect ():
    client.settimeout(20)  #设置连接超时时间
    time.sleep(0.2)
    try:
        print("try recv data...")
        data, addr = client.recvfrom(64)  #从服务器接收数据  
        print(b"recv: " + data)
        if b'open' in  data:  
            DataFlag = data[9:13]
            SendData = b'005532A01' +  DeviceID + MM  + DataFlag + b'09' + UserID + b'OK05'
            print(b"sendto: " + SendData)
            servo1.init(duty = 20)
            servo2.init(duty = 20)
            client.sendto(SendData, UDP_server_addr)  #向服务器发送数据转为bytes
            time.sleep(4)
            servo1.duty(130)
            servo2.duty(130)
            time.sleep(1)
            servo1.deinit()
            servo2.deinit()
        else:
            pass
    except:
        client.sendto(Heart, UDP_server_addr)  #向服务器发送心跳包  
        print("sendto heart:" + Heart)
if __name__=='__main__':
    time.sleep(1)
    do_connect()
    shakeHand_UDP_server()
    while True:
        revMsgAndKeepConnect()
	
	
	
	
	
	
	
	