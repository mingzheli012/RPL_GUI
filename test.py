import socket
def isOpen(ip,port):
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   try:
      s.connect((ip, int(port)))
      s.shutdown(1)
      return True
   except:
      return False

full_ip = '128.111.127.97:339'
ip = full_ip[0:full_ip.find(':')]
print(ip)
port = full_ip[full_ip.find(':')+1:len(full_ip)]
print(port)

print(isOpen(ip,port))
