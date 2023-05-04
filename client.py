import socket
from datetime import datetime, timedelta

#import poplib
import ssl


def get_emails():    
    hostname = 'pop.gmail.com'
    context = ssl.create_default_context()

    with socket.create_connection((hostname, 995)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            #print(ssock.version())

            response = ssock.recv(1024)
            print(response.decode())

            ssock.send((b'USER jake.dev.mileham@gmail.com\r\n'))
            response = ssock.recv(1024)
            print(response.decode())

            ssock.send((b'PASS xxxxxxxxxxxx\r\n'))
            response = ssock.recv(1024)
            print(response.decode())

            ssock.send(f'LIST\n'.encode())
            response = ssock.recv(1024)
            print(response.decode())

            ssock.send(f'RETR 4\n'.encode())
            response = ssock.recv(2048)
            print(response.decode())

            ssock.send((b'QUIT\r\n'))
            response = ssock.recv(1024)
            print(response.decode())

        ssock.close()

    return



def main():
    get_emails()
    return


if __name__ == '__main__':
    main()

    