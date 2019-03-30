
#pass: r********p****5
import os
import socket
import time



def Main():

	port = 5004
	IDENTIFIER = "kill"
	HOMESEC_IP = 'localhost'

	host = "0.0.0.0"

	s = socket.socket()
	s.bind(('', port))

	s.listen(1)

	print(f"[+] Server started with host:port --> {host}:{port}")

	while True:

		print("[+] Server Running...")
		c, addr = s.accept()
		print("[+] Client with ip ", addr, " connected")
		request = c.recv(1024)
		request = request.decode("utf-8")

		if request == "get":

			IDENTIFIER = IDENTIFIER.encode()
			c.send(IDENTIFIER)


			file_number = 0
			while True:

				path, dirs, files = next(os.walk("images"))
				filecount = str(len(files))
				c.send(filecount.encode().strip())

				file_number = 0
				for file in files:

					file_number += 1
					print("[+] Downloading file ", file_number, " ===============================")
					filesize = str(os.path.getsize(f"images/{file}"))

					print("[+] Sending file with filesize: ", filesize)
					c.send(filesize.encode().strip())
					filesize = int(filesize)

					with open(f"images/{file}", "rb") as f:

						bytes_to_send = f.read(1024)
						c.send(bytes_to_send)
						total_bytes_sent = len(bytes_to_send)
						while total_bytes_sent < filesize:
							time.sleep(0.05)
							print("Progress ", total_bytes_sent, "/", filesize)
							bytes_to_send = f.read(1024)
							c.send(bytes_to_send)
							total_bytes_sent += len(bytes_to_send)
						f.close()
						os.remove(f"images/{file}")

				remaining_files = os.listdir("images/")
				while len(remaining_files) == 0:
					print("[-] No new activity. Standing by...")
					remaining_files = os.listdir("images/")
					time.sleep(10)
		else:
			c.send("[-] Error. Invalid Request".encode().strip())

	s.close()



if __name__ == "__main__":
	Main()
