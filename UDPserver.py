import time
import base64
import socket
import network
import camera

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect("iPhone de Jasson", "Jasson198516")
    
ticks1 = time.ticks_ms()

BUFF_SIZE = 65536
server_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
# server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
# server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)

while not station.isconnected():
    ticks2 = time.ticks_ms()
    if time.ticks_diff(ticks1, ticks2) % 10000 == 0:
        print("Conectando...")
    
print('Conexión exitosa')
print(station.ifconfig())

host_ip = station.ifconfig()[0]
print(host_ip)
port = 9999
socket_address = (host_ip,port)
server_socket.bind(socket_address)
print('Listening at:',socket_address)

try:
    camera.deinit()
    camera.init(0, format=camera.JPEG, fb_location=camera.PSRAM)
except Exception as e:
    print(e)
    

print('waiting....')
data,addr=server_socket.recvfrom(1024)
print('GOT connection from ',addr)
while True:
    

        buffer =camera.capture()
#         print(len(buffer))
        message = base64.b64encode(buffer)
#         print(len(message))
        server_socket.sendto(message,addr)
#         print('holi')
        time.sleep(.1)

    