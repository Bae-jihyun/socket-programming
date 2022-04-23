from socket import *

HOST = "127.0.0.1"
PORT = 9999

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((HOST, PORT))
for _ in range(10):
    data = input("bye: connection close, case: upper/lower case, signUp, signIn      ").strip()
    clientSocket.sendall(data.encode())
    msg = clientSocket.recv(1024).decode()
    print('From Server: ', msg)

    if (data.split()[0] == 'signUp') or (data.split()[0] == 'signIn'):
        if msg == "이미 존재하는 ID입니다." or msg == "존재하지 않는 ID입니다.":
            continue
        while True:
            pw = input("pw를 입력해주세요 : ")
            clientSocket.send(pw.encode())
            success = clientSocket.recv(1024).decode()
            print('From Server: ', success)
            if "Success" in success:
                break

    if data == "bye":
        break

clientSocket.close()
