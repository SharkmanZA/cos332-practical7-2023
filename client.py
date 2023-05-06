import socket
from datetime import datetime, timedelta
import re
import ssl

HOST, PORT = '127.0.0.1', 1025

SENDER = 'jake.dev.mileham@gmail.com'

EMAIL = 'jake.dev.mileham@gmail.com'
#app pasword used for POP3 to access emails
PASSWORD = ''

def send_email_to_sender(contents):
    print(f'\033[32mSending Email to: {contents[1]}\033[0m\n')
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    my_socket.connect((HOST,PORT))

    MSG = 'From: ' + SENDER + '\r\nTO: ' + contents[1] + '\r\nSubject: Important announcement\r\n\r\n' +  SENDER  + ' is on vaction currently!' + '\r\n.\r\n'

    my_socket.send(('HELO ' + SENDER + '\r\n').encode())
    response = my_socket.recv(1024)
    print(response.decode())

    my_socket.send(('MAIL FROM:<' + SENDER + '>\r\n').encode())
    response = my_socket.recv(1024)
    print(response.decode())

    my_socket.send(('RCPT TO:<' + contents[1] +'>\r\n').encode())
    response = my_socket.recv(1024)
    print(response.decode())

    my_socket.send(b'DATA\r\n')
    response = my_socket.recv(1024)
    print(response.decode())

    my_socket.send(MSG.encode())
    response = my_socket.recv(1024)
    print(response.decode())

    my_socket.send(b'QUIT\r\n')
    response = my_socket.recv(1024)
    print(response.decode())

    my_socket.close()
    print("✅ Sent")
    
    return

#Find all emails that have the subject 'prac7' as they are important
def find_all_emails(emails, ssock):
    print("===================================================")
    print("WAITING EMAILS")
    print("===================================================\n")

    with open('valid.txt', 'w') as f:
        f.seek(0)
        rows = 0
        for id, size in emails.items():
            ssock.send(f'TOP {id} 1\n'.encode())
            response = ssock.recv(1024).decode()
            msg = ""
            msg += response
            while response.endswith(".\r\n") == False:
                response = ssock.recv(1024).decode()
                if(response != ""):
                    msg += response
            sender  = re.search(r"from:.*?<([^>]+)>", msg, flags=re.IGNORECASE)
            subject = re.search(r'Subject: (.+?)\r\n', msg, flags=re.IGNORECASE)
            contents = [str(id), sender.groups(0)[0], subject.groups(0)[0], str(size)]

            GREEN = '\033[92m'
            RED = '\033[91m'
            END = '\033[0m'
            color = GREEN if contents[2] == "prac7" else RED

            # Clearly idk how format works
            if(subject.groups(0)[0] == 'prac7'):
                

                print(f'✅ {contents[0]}. Sender: {contents[1]} Subject: {color}{contents[2]}{END} Size: {contents[3]}')
                f.write(f"{';'.join(contents)}\n")
                rows = rows + 1
            else:
                print(f'❌ {contents[0]}. Sender: {contents[1]} Subject: {color}{contents[2]}{END} Size: {contents[3]}')

    f.close()
    print("\n===================================================\n\n")
    return rows


def get_emails():    
    hostname = 'pop.gmail.com'
    context = ssl.create_default_context()

    with socket.create_connection((hostname, 995)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:

            response = ssock.recv(2048)
            print(response.decode())

            ssock.send((f'USER {EMAIL}\r\n').encode())
            response = ssock.recv(2048)
            print(response.decode())

            ssock.send((f'PASS {PASSWORD}\r\n').encode())
            response = ssock.recv(2048)
            print(response.decode())

            ssock.send(f'LIST\n'.encode())
            response = ssock.recv(2048)
            print(response.decode())
            

            emails = list(map(str.strip, response.decode().split("\n")[1:-2]));
            email_values = {email.split()[0]: email.split()[1] for email in emails}
            
            response = find_all_emails(email_values, ssock)
            if(response == 0):
                print("NOT VALID EMAILS")
                ssock.send((b'QUIT\r\n'))
                response = ssock.recv(2048)
                print(response.decode())
                ssock.close()
                return

            #For all emails that are valid, email the sender stating you are on vaction 🥳🥳🥳🥳🥳
            with open('valid.txt', 'r') as f:
                f.seek(0)
                emails = f.readlines()
                for email in emails:
                    contents = list(email.split(";"))
                    #print(f'{contents[0]}. Sender: {contents[1]} Subject: {contents[2]} Size: {contents[3]}')
                    send_email_to_sender(contents)
            f.close()

            print("Type out the emails you would like to delete, eg. 1,2,3,4 or type NONE: ")
            ids_input = input()
            if ids_input != 'NONE':
                ids = list(ids_input.split(","))
                for id in ids:
                    ssock.send((f'DELE {int(id)}\r\n').encode())
                    response = ssock.recv(2048)
                    print(response.decode())

            ssock.send((b'QUIT\r\n'))
            response = ssock.recv(2048)
            print(response.decode())

            ssock.close()

    return



def main():
    get_emails()
    return


if __name__ == '__main__':
    main()


#TODO
#1. Use RETR to remvoe from POP3 server