# COS332 Practical 7 2023

The task was to retrieve emails from a POP3 server using POP3 commands. These emails must be filtered by subject and then senders of emails whose subject was 'prac7' must be notified that the current recipient is on vaction.

---

## POP3 Server
To read from my gmail account I used the [ssl wrapper](https://docs.python.org/3/library/ssl.html) library

This provided a secure connection to the gmail POP3 server so I could use my credentials.

---

## SMTP Server
I used [mailhog](https://github.com/mailhog/MailHog) to send dumby mail to my senders.

---
