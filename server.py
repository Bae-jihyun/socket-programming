from socket import *

HOST = "127.0.0.1"
PORT = 9999

serverSocket = socket(AF_INET, SOCK_STREAM)  # create control connection socket (IP4, TCP 사용)
serverSocket.bind((HOST, PORT))
serverSocket.listen(1)  # 1개 client를 기다리는 중
print("The server is ready to receive client")

connectionSocket, addr = serverSocket.accept()  # data connection socket
dic = {"govl6113": "gogobebe132!"}
while True:
    command = connectionSocket.recv(1024).decode()
    lst = command.split()

    if lst[0] == "bye":  # connection close
        connectionSocket.sendall("connection close".encode())
        break

    if lst[0] == "case":  # upper, lower case
        print("case")
        if lst[1].isupper():
            afterData = lst[1].lower()
        else:
            afterData = lst[1].upper()
        connectionSocket.sendall(afterData.encode())
        continue

    if lst[0] == 'signUp':  # login ID
        if dic.get(lst[1]) is None:
            connectionSocket.sendall("ok. PW?".encode())
            pw = connectionSocket.recv(1024).decode()
            ## 조건식
            dic[lst[1]] = pw
            connectionSocket.sendall("signUp Success.".encode())
        else:
            connectionSocket.sendall("이미 존재하는 ID입니다.".encode())
        continue

    if lst[0] == 'signIn':  # login PW
        if dic.get(lst[1]) is not None:
            connectionSocket.sendall("ok. PW?".encode())
            pw = connectionSocket.recv(1024).decode()
            if dic.get(lst[1]) == pw:
                connectionSocket.sendall("signIn Success.".encode())
            else:
                connectionSocket.sendall("pw가 알맞지 않습니다.".encode())
        else:
            connectionSocket.sendall("존재하지 않는 ID입니다.".encode())
        continue

    else:
        connectionSocket.sendall("정확한 입력을 해주시기 바랍니다.".encode())

print("connection close")
connectionSocket.close()
print("Server close")
serverSocket.close()
