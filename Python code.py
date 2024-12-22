import socket
import threading
import multiprocessing
pc_host=""
camera_host="10.32.38.13"
def Process1 (pc_port, camera_port):
    def one (sender, receiver):
       while True:
           try:
               request = sender.recv(2048)
               receiver.sendall(request)
           except:
               break
       sender.close()
       receiver.close()
    def two (sender, receiver):
       while True:
           try:
               response = receiver.recv(2048)
               sender.sendall(response)
           except:
               break
       sender.close()
       receiver.close()

    s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s1.bind((pc_host, pc_port))
    s1.listen(5)
    while True:
      client_socket, client_address = s1.accept()
      c2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      c2.connect((camera_host, camera_port))
      t1 = threading.Thread(target=one,args=(client_socket, c2))
      t2 = threading.Thread(target=two,args=(client_socket, c2))
      t1.start()
      t2.start()

def Process2 (pc_port, camera_port):
    def one(sender, receiver):
            while True:
                try:
                    request = sender.recv(2048)
                    receiver.sendall(request)
                except:
                    break
            sender.close()
            receiver.close()
    def two(sender, receiver):
        while True:
            try:
                response = receiver.recv(2048)
                sender.sendall(response)
            except:
                break
        sender.close()
        receiver.close()

    s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s1.bind((pc_host, pc_port))
    s1.listen(5)
    s3 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s3.bind(('',7788))
    while True:
      client_socket, client_address = s1.accept()
      c2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      c2.connect((camera_host, camera_port))
      t1 = threading.Thread(target=one,args=(client_socket, c2))
      t2 = threading.Thread(target=two,args=(client_socket, s3))
      t1.start()
      t2.start()

class control (multiprocessing.Process):
    def __init__(self, pc_port, camera_port):
        multiprocessing.Process.__init__(self)
        self.pc_port=pc_port
        self.camera_port=camera_port
    def run(self):
        Process1(self.pc_port, self.camera_port)

class video_transmission (multiprocessing.Process):
    def __init__(self, pc_port, camera_port):
        multiprocessing.Process.__init__(self)
        self.pc_port=pc_port
        self.camera_port=camera_port
    def run(self):
        Process2(self.pc_port, self.camera_port)

if __name__=='__main__':
    p1 = control(80,80)
    p2 = video_transmission(50010,50010)
    p1.start()
    p2.start()