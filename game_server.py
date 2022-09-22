import socket, random
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('127.0.7.1', 5051))
client = []

size = 500

gx = 25 #random.randint(1, int(500 / 50)) * 50 - 25
gy = 25 #random.randint(1, int(500 / 50)) * 50 - 25

while 1:
     data, addres = sock.recvfrom(1024)
     print(addres[0], addres[1], data, client)
     if addres not in client:
         client.append(addres)
     for clients in client:
         if data.decode("utf-8")=="GG":
             gx = random.randint(1, int(size / 50)) * 50 - 25
             gy = random.randint(1, int(size / 50)) * 50 - 25
             continue
         print(clients)
         if clients == addres:
             continue
         data = (data.decode("utf-8")+f"${gx}:{gy}").encode("utf-8")
         print(data)
         sock.sendto(data, clients)
         print(gx, gy)


