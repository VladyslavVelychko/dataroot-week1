import os, webbrowser, socket
from pathlib import Path


def basic():
    def send_answer(conn, status="200 OK", typ="text/plain; charset=utf-8", data=""):
        data = data.encode("utf-8")
        conn.send(b"HTTP/1.1 " + status.encode("utf-8") + b"\r\n")
        conn.send(b"Server: simplehttp\r\n")
        conn.send(b"Connection: close\r\n")
        conn.send(b"Content-Type: " + typ.encode("utf-8") + b"\r\n")
        conn.send(b"Content-Length: " + bytes(len(data)) + b"\r\n")
        conn.send(b"\r\n")# after empty str in HTTP begins data
        conn.send(data)

    def parse(conn, addr):# connection
        data = b""
    
        while not b"\r\n" in data: # wait for first string
            tmp = conn.recv(1024)
            if not tmp:   # empty object, socket close
                break
            else:
                data += tmp
    
        if not data:
            return
        
        udata = data.decode("utf-8")
    
        # only first string
        udata = udata.split("\r\n", 1)[0]
        # split our string
        method, address, protocol = udata.split(" ", 2)
    
        if method != "GET":
            send_answer(conn, "404 Not Found", data="Not Found")
            return

        answer = """<!DOCTYPE html>"""
        answer += """<html><head><title>Files and directories</title></head><body><ul>"""
        for i in os.listdir(os.getcwd()):
            answer=answer+os.getcwd()+"/"+i
            answer+="""<li><a href='#'>show content</a></li>"""
            webbrowser.open("file://"+os.getcwd()+"/"+i)
            answer+="<br>"
            #def clicked():
                #return webbrowser.open("file://"+os.getcwd()+"/"+i)
        answer += """</ul></body></html>"""
    
        send_answer(conn, typ="text/html; charset=utf-8", data=answer)

    sock = socket.socket()
    sock.bind( ("", 8080) )
    sock.listen(5)

    try:
        while True:
            conn, addr = sock.accept()
            print("New connection from " + addr[0])
            try:
                parse(conn, addr)
            except:
                send_answer(conn, "500 Internal Server Error", data="There is an error occured.")
            finally:
                conn.close()
    finally: sock.close()

url="/index.html"
my_file=Path(os.getcwd()+url)
if my_file.is_file():
    webbrowser.open("file://"+os.path.realpath(os.getcwd()+url))
else:
    basic()