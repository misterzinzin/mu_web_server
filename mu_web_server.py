try:
  import usocket as socket
except:
  import socket
  
import network
import _thread
import os
import sys

class webserver_global:
    pass

class mu_web_server:
    # static functions
    def file_exists(filename):
        try:
            return (os.stat(filename)[0] & 0x4000) == 0
        except OSError:
            return False
    def web_page_404():
        html = """<html><head> <title>404 not found</title></head><body> <h1>404 not found</h1></body></html>"""
        return html
    
    #instance functions
    def __init__(self):
        self.globalVar = webserver_global()
        self.pageFunctions = {}
    def start(self):
        _thread.start_new_thread(self.doServe,())
    def doServe(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', 80))
        s.listen(5)
        while True:
            try:
                conn, addr = s.accept()
                #print('Got a connection from %s' % str(addr))
                _thread.start_new_thread(self.serveClient,(conn,addr))
            except:
                conn.close()
        
        
    def serveClient(self,conn,addr):
        request = conn.recv(1024)
        request = request.decode('utf-8')
        req = request.split('\n')[0]
        reqs = req.split()
        if reqs[0] == 'GET' and reqs is not None and len(reqs) >= 2:
            temp = reqs[1].split('?')
            page = temp[0]
            pageArgs = []
            if len(temp) >= 2:
                pageArgs = temp[1].split('&')
            
            #print('page = %s' % page)
            #print('args=',pageArgs)
            if page in self.pageFunctions:
                response = self.pageFunctions[page](self.globalVar,pageArgs)
                conn.send('HTTP/1.1 200 OK\n')
                conn.send('Content-Type: text/html\n')
                conn.send('Connection: close\n\n')
                conn.sendall(response)
            else:
                
                if webserver.file_exists(page):
                    #print("file exist")
                    conn.send('HTTP/1.1 200 OK\n')
                    conn.send('Content-Type: text/html\n')
                    conn.send('Connection: close\n\n')
                    f = open(page,'rb')
                    while True:
                        bytes_read = f.read(1024)
                        if not bytes_read:
                            break
                        conn.sendall(bytes_read)
                else:
                    #print("file do not exists")
                    response = webserver.web_page_404()
                    conn.send('HTTP/1.1 404 Not Found\n')
                    conn.send('Content-Type: text/html\n')
                    conn.send('Connection: close\n\n')
                    conn.sendall(response)
        conn.close()
          

    
      
#doServe()

