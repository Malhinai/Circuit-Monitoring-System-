# a function that takes text and key and returns the encrypted text in aes-128-ecb mode

def encrypt(text, key):
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import pad, unpad
    cipher = AES.new(key, AES.MODE_ECB)
    padded = pad(text.encode('utf-8'), AES.block_size)
    return cipher.encrypt(padded)

# a function that takes text and key and returns the decrypted text in aes-128-ecb mode

def decrypt(text, key):
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import unpad
    cipher = AES.new(key, AES.MODE_ECB)
    return unpad(cipher.decrypt(text), AES.block_size).decode('utf-8')


# a function thst sends a text through tcp port :

def senddata(ipaddrs,text, port):
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s. connect((ipaddrs, port))
    s.send(text,1024)
    s.close()


# a function that receives data from tcp port and assigns it to a variable:
def receive(ipaddrs,port):
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ipaddrs, port))
    data = s.recv(1024)
    s.close()
    return data

