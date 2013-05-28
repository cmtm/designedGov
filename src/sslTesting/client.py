import socket, ssl, pprint

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# require a certificate from the server
ssl_sock = ssl.wrap_socket(s,
						   certfile="../keysAndCerts/certificates/client1.crt",
                           ca_certs="../keysAndCerts/certificates/myCA.crt",
                           keyfile="../keysAndCerts/keys/client1.pem",
                           cert_reqs=ssl.CERT_REQUIRED)

ssl_sock.connect(('localhost', 10023))

print(repr(ssl_sock.getpeername()))
print(ssl_sock.cipher())
print(pprint.pformat(ssl_sock.getpeercert()))

if ssl_sock.getpeercert()['subject'][0][0][1] != u'9F32383582053809':
	raise Exception("Certificate contains wrong userID")

# Set a simple HTTP request -- use httplib in actual code.
ssl_sock.sendall("""Hi there""")

# Read a chunk of data.  Will not necessarily
# read all the data returned by the server.
data = ssl_sock.recv(16384)
print(data)

# note that closing the SSLSocket will also close the underlying socket
ssl_sock.close()
