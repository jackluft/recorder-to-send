#Run two of these files on python3
import socket
import pickle
import sounddevice as sd 
import threading
import time
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Enter in a host name that u have
host = ''
port = 4579
s.connect((host,port))
print("connected to server")
fs = 16000
def recv_data():
	
	while True:
		size = s.recv(10).decode('UTF-8')
		data = b""
		data_size = 0
		while data_size < int(size):
			if (data_size+4096) > int(size):
				re = s.recv(int(size)-data_size)
			else:
				re = s.recv(4096)
			data+=re
			data_size+=len(re)

		print("All Data recieved")

		sound = pickle.loads(data)
		print("Playing sound")
		sd.play(sound,fs)
		sd.wait()
		print("Done")
		print("How many seconds do you want your recording?")


def user():

	print("Welcome to recorder sender!!1")
	print("Follow the steps below to send a record message")
	while True:
		print("How many seconds do you want your recording?")
		sec = input()
		while(sec.isnumeric() == False):
			print("Please enter a NUMBER")
			sec = input()
		sec = int(sec)


		print("The recording with be "+str(sec)+"'s longth")
		print("Press Enter to start recording")
		nothing = input()
		print("\n")
		#If this doesn't work this might be the problem
		#Might need to change the microphone channel

		print("Recording on")
		data = sd.rec(int(sec*fs),fs,1)
		sd.wait()
		print("Recording Stops")
		mess = pickle.dumps(data)

		#Sends the size of the recording

		size = format(len(mess), '010d')
		s.send(size.encode('UTF-8'))

		#Sends the Data of the recording
		
		s.send(mess)
		print("Recording sent")

threading.Thread(target=user).start()
threading.Thread(target=recv_data).start()
while True:
	time.sleep(0.5)

s.close()











