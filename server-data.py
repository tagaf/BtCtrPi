from bluetooth import *
import matplotlib.pyplot as plt
import numpy as np
server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

advertise_service( server_sock, "SampleServer",
                   service_id = uuid,
                   service_classes = [ uuid, SERIAL_PORT_CLASS ],
                   profiles = [ SERIAL_PORT_PROFILE ], 
#                   protocols = [ OBEX_UUID ] 
                    )
                   
print("Waiting for connection on RFCOMM channel %d" % port)

client_sock, client_info = server_sock.accept()
print("Accepted connection from ", client_info)
t = np.arange(0., 5.,0.05) 
try:
    while True:
        line = client_sock.recv(1024)
        if len(data) == 0: break
	data=line.split(',')
	i=i+1
	if i == 100
		j=0
		for j<100
			plt.plot((float) data,t,'r--')
			plt.show()
			break
        print("received [%s]" % line)
except IOError:
    pass

print("disconnected")

client_sock.close()
server_sock.close()
print("all done")
