
import os
import socket
import time



def Main():

	host = "localhost"
	port = 5004

	s = socket.socket()
	s.bind((host, port))

	s.listen(1)

	while True:

		c, addr = s.accept()
		print("Client with ip ", addr, " connected")
		request = c.recv(1024)
		request = request.decode("utf-8")
		if request == "get":

			path, dirs, files = next(os.walk("images"))
			filecount = str(len(files))
			c.send(filecount.encode())

			for file in files: 

				print("DONKEY")
				filesize = str(os.path.getsize(f"images/{file}"))

				print("Sending file with filesize: ", filesize)
				c.send(filesize.encode())
				filesize = int(filesize)

				with open(f"images/{file}", "rb") as f:

					bytes_to_send = f.read(1024)
					c.send(bytes_to_send)
					total_bytes_sent = len(bytes_to_send)
					while total_bytes_sent < filesize:
						time.sleep(0.2)
						print("Progress ", total_bytes_sent, "/", filesize)
						bytes_to_send = f.read(1024)
						c.send(bytes_to_send)
						total_bytes_sent += len(bytes_to_send)
					f.close()

		else:
			c.send("Error. Invalid request".encode())

	s.close()



if __name__ == "__main__":
	Main()
