
import socket
import time 


def Main():

	host = "10.0.0.138"
	port = 5003

	s = socket.socket()
	s.connect((host, port))

	request = input("Type request: ")
	request = request.encode()
	s.send(request)

	if request != "q":
	

		while True:

			filecount = s.recv(1024).decode("utf-8")
			print("Downloading ", filecount, " files")

			for file in range(int(filecount)):

				filesize = s.recv(1024).decode("utf-8")
				filesize = int(filesize)
				print("Downloading file with filesize: ", filesize)

				timestamp = str(time.time())

				f = open(f"images/new_{timestamp}.jpg", "wb")
				data = s.recv(1024)
				total_recieved = len(data)
				f.write(data)
				
				while total_recieved < filesize:
					data = s.recv(1024)
					total_recieved += len(data)
					f.write(data)
					print("Progress: ", total_recieved, "/", filesize)
					
				f.close()

		print("Download complete!")

	

	s.close()



if __name__ == "__main__":

	Main()