from socket import *

HOST = "127.0.0.1"
PORT = 9999

clientSocket = socket(AF_INET, SOCK_STREAM)  # socket 생성 (IP4, TCP 사용)
clientSocket.connect((HOST, PORT))           # server와 연결
try:
    while True:
        # 사용자 입력
        data = input("bye: connection close, case: upper/lower case, signUp, signIn      ").strip()
        clientSocket.sendall(data.encode())         # server에 메세지 송신
        msg = clientSocket.recv(1024).decode()      # server로부터 메세지 수신
        print('From Server: ', msg)

        # signIn, signUp process
        if ((data.split()[0] == 'signUp') or (data.split()[0] == 'signIn')) \
                and not msg == "아이디가 입력되지 않았습니다.":
            if msg == "이미 존재하는 ID입니다." or msg == "존재하지 않는 ID입니다.":
                continue
            while True:
                pw = input("pw를 입력해주세요 : ")
                clientSocket.send(pw.encode())
                resultPwdCheck = clientSocket.recv(1024).decode()
                print('From Server: ', resultPwdCheck)
                if "Success" in resultPwdCheck:
                    break

        # connection close
        if data == "bye":
            break
except KeyboardInterrupt:
    print("KeyboardInterrupt가 발생해 종료됩니다.")
finally:
    clientSocket.close()
