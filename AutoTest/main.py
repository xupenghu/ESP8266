# main.py
import network
import webrepl
import time
from machine import Pin	#导入GPIO模块

SSID = "U05E-000016"
PASSWORD = "1223334444"
wlan = network.WLAN(network.STA_IF)	
relay0 = Pin(16, Pin.OUT)    # create output pin on GPIO16
relay0.value(1)				 #关闭开关
time.sleep(1)

#全局变量定义
ErrorCount = 0 		#失败计数
SuccessCount = 0 	#成功计数
TotalCount = 0		#总计数

#路由器自动测试函数
def router_autotest(): 
	#全局变量申明
	global SuccessCount
	global ErrorCount
	
	relay0.value(1) 	#下电
	time.sleep(2)
	relay0.value(0)  #上电
	time.sleep(30)	 #等待30s 
	wlan.active(True)
	if not wlan.isconnected():
		print('connecting to network...')
		wlan.connect(SSID, PASSWORD)
	time.sleep(10) 	#再等待10s
	#如果还没有连上 则继续等待最多30s
	start = time.time()
	while not wlan.isconnected():
		time.sleep(5)
		if time.time() - start > 6:
			print("Error! Wifi hotspot is not established.\n")
			ErrorCount += 1 #失败计数
			break
			
	if wlan.isconnected():
		SuccessCount += 1 #成功计数
		print("Success!\n")
		
	relay0.value(1)			#下电
	
#系统自动测试函数
def system_autotest(): 
	#全局变量申明
	global SuccessCount
	global ErrorCount
	
	#开机
	relay0.value(0)  #上电
	time.sleep(6)	 #等待6s 等待系统开机
	relay0.value(1)  #开机完成
	
	wlan.active(True)
	if not wlan.isconnected():
		print('connecting to network...')
		wlan.connect(SSID, PASSWORD)
	time.sleep(40) 	#再等待40s 等中继的热点起来
	#如果还没有连上 则继续等待最多30s
	start = time.time()
	while not wlan.isconnected():
		time.sleep(5)
		if time.time() - start > 6:
			print("Error! Wifi hotspot is not established.\n")
			ErrorCount += 1 #失败计数
			break
			
	if wlan.isconnected():
		SuccessCount += 1 #成功计数
		print("Success!\n")
		
	#关机
	relay0.value(0)  #上电
	time.sleep(6)	 #等待6s 等待系统开机
	relay0.value(1)  #关机完成
	
	time.sleep(10)		#等待关机彻底完成
	
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


if __name__ == '__main__':
	print('start testing...')
	while True:
		system_autotest()
		TotalCount +=1
		print('TotalCount : ', TotalCount)
		print('SuccessCount : ', SuccessCount )
		print('ErrorCount : ', ErrorCount)
		print('Success rate :', (SuccessCount/TotalCount)*100, '%\n')
		time.sleep(1)





















