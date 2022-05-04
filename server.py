from socket import *
import re

HOST = "127.0.0.1"
PORT = 9999


def passwordCheck(pw):
    if len(pw) < 8:
        return "패스워드 길이는 8자 이상이어야 합니다."
    if not re.search("[a-z]", pw) and not re.search("[A-Z]", pw):
        return "영문자가 포함되어 있어야 합니다."
    if not re.search("[0-9]", pw):         # search는 문자열 전체를 검색해 정규식과 매칭되는지 검사한다.
        return "최소 1개 이상의 숫자가 포함되어야 합니다."
    if not re.search("[`!@#$%^&*(),<.>/?+]", pw):
        return "최소 1개 이상의 특수문자가 포함되어야 합니다."
    else:
        return "success"

# id/pw 저장 dic
dic = {"Bae-jihyun": "baejibaeji13@",
       "govl6113": "gogobebe132!",
       "himitery": "password1@#",
       "hohohaha": "enjoyhaha132#",
       "goji": "hoas2453f#",
       }

serverSocket = socket(AF_INET, SOCK_STREAM)  # control connection socket 생성 (IP4, TCP 사용)
serverSocket.bind((HOST, PORT))              # 생성된 socket에 HOST와 PORT 맵핑
serverSocket.listen(1)                       # 1개 client를 기다리는 중
print("The server is ready to receive client")
connectionSocket, addr = serverSocket.accept()  # client와 연결된 data connection socket 생성
try:
    while True:
        # client로부터 메세지 수신을 대기
        command = connectionSocket.recv(1024).decode()
        lst = command.split()

        if lst[0] == "bye":  # connection close
            connectionSocket.sendall("connection close".encode())
            break

        if lst[0] == "case":  # upper, lower case
            print("reqeust: ===== case =====")
            if lst[1].isupper():
                afterData = lst[1].lower()
            else:
                afterData = lst[1].upper()
            connectionSocket.sendall(afterData.encode())  # client에 메세지 전송
            continue

        if lst[0] == 'signUp':  # signUp
            print("request: ===== signUp =====")
            try:
                if dic.get(lst[1]) is None:  # 만약 Id가 dic(DB)에 없다면
                    connectionSocket.sendall("ok. PW?".encode())
                    while True:
                        # pw가 정규식 통과 될 때까지 검사
                        pw = connectionSocket.recv(1024).decode()
                        resultPwdCheck = passwordCheck(pw)
                        if resultPwdCheck in "success":
                            break
                        else:
                            connectionSocket.sendall(resultPwdCheck.encode())
                    dic[lst[1]] = pw  # Id, PW dic에 저장
                    connectionSocket.sendall("signUp Success.".encode())
                else:
                    connectionSocket.sendall("이미 존재하는 ID입니다.".encode())
            except IndexError:
                connectionSocket.sendall("아이디가 입력되지 않았습니다.".encode())
            finally:
                continue

        if lst[0] == 'signIn':  # login
            print("request: ===== signIn ======")
            try:
                if dic.get(lst[1]) is not None:  # 만약 id가 있다면
                    connectionSocket.sendall("ok. PW?".encode())
                    while True:
                        # pw 확인
                        pw = connectionSocket.recv(1024).decode()
                        if dic.get(lst[1]) == pw:
                            # login 성공
                            connectionSocket.sendall("signIn Success.".encode())
                            break
                        else:
                            connectionSocket.sendall("pw가 알맞지 않습니다.".encode())
                else:
                    connectionSocket.sendall("존재하지 않는 ID입니다.".encode())
            except IndexError:
                connectionSocket.sendall("아이디가 입력되지 않았습니다.".encode())
            finally:
                continue

        else:
            connectionSocket.sendall("정확한 입력을 해주시기 바랍니다.".encode())
except (ConnectionAbortedError, IndexError):
    print("client에 의해 중단되었습니다.")
finally:
    print("connection close")
    connectionSocket.close()
    print("Server close")
    serverSocket.close()