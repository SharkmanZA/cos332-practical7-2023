# COS332 Practical 7 2023

The task was to retrieve emails from a POP3 server using POP3 commands. These emails must be filtered by subject and then senders of emails whose subject was 'prac7' must be notified that the current recipient is on vaction. I have used my gmail account therefore using gmails POP3 server.

---

## POP3 Server
To read from my gmail account I used the [ssl wrapper](https://docs.python.org/3/library/ssl.html) library

This provided a secure connection to the gmail POP3 server so I could use my credentials.

---

## SMTP Server
I used [mailhog](https://github.com/mailhog/MailHog) to send dumby mail to my senders.

---

## SETUP
1. Download Source Code
2. Install mailhog
3. Run mainhog 
  - Example: 'brew services start mailhog'
4. Set EMAIL and SENDER field to your email
5. Set PASSWORD field to your gmail app password
6. Run Script
  - Example: 'python client.py'
7. If valid mail with subject 'prac7' you will see it in your mailhog inbox at localhost:8025

---
