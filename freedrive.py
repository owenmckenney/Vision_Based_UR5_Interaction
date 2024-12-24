# File to put UR5 into freedrive mode

import socket

ip = "10.168.18.25"  
port = 30002       

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.connect((ip, port))
    print("Connected to UR5.")
except Exception as e:
    print(f"Connection error: {e}")
    exit(1)

urscript_command = '''
def freedrive_and_log():    
    while True:
        freedrive_mode()
    end
end
freedrive_and_log()
'''

try:
    sock.sendall(urscript_command.encode('utf-8'))
    print("Freedrive and logging script sent to UR5.")
except Exception as e:
    print(f"Error sending URScript command: {e}")

sock.close()
print("Socket closed.")
