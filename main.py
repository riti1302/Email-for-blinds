import smtplib
import time
import imaplib
import email
from Tkinter import *

def read_email_from_gmail():

    ORG_EMAIL   = "@gmail.com" 
    FROM_EMAIL = email.get()
    FROM_PWD    = password.get()
    SMTP_SERVER = "imap.gmail.com"
    SMTP_PORT   = 993
    try:
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(FROM_EMAIL,FROM_PWD)
       #lists = mail.list()
       #print lists
        mail.select('inbox')

        result, data = mail.search(None, '(SINCE "16-Aug-2018" BEFORE "17-Aug-2018")')
        mail_ids = data[0]

        id_list = mail_ids.split()
        print id_list 
        first_email_id = int(id_list[0])
        latest_email_id = int(id_list[-1])
        print "success"

        for i in range(latest_email_id,first_email_id, -1):
            typ, data = mail.fetch(i, '(RFC822)' )
            print "Success 2"
            raw_email = data[0][1]
            raw_email_string = raw_email.decode('utf-8')
            print "Success 3"
            for response_part in data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_string(response_part[1])
                    email_subject = msg['subject']
                    email_from = msg['from']
                    email_date = msg['date']
                    print 'From : ' + email_from + '\n'
                    print 'Subject : ' + email_subject + '\n'
                    print 'Date : ' + email_date +'\n'
            email_message = email.message_from_string(raw_email_string)
            for part in email_message.walk():
                if part.get_content_type() == "text/plain":
                    print "Success 4"
                    body = part.get_payload()
                    print "Success 5"
                    print "content: " + str(body)
                elif part.get_content_type() == "text/html":
                    print "The email consist of a link."
                else:
                    print "The email has non-readable file"
                   
                    
    except:
        print "Error"


root = Tk()
root.geometry('400x200')
root.title('Email selector')
root.configure()

#Email icon
icon = PhotoImage(file = 'Email_icon.gif')
email_icon = Label(root, image= icon, justify = LEFT)
email_icon.grid(column = 1)

#Entry for email address and password
Label(root, text = "Email-address", justify = LEFT).grid(row=2, padx = 10, pady = 10)
Label(root, text = "Password", justify = LEFT).grid(row=3, padx = 10)
email = Entry(root, justify = LEFT, width = 30)
password = Entry(root, justify = LEFT, show = '*', width = 30)
email.grid(row=2, column=1, padx = 10, pady = 10)
password.grid(row=3, column=1, padx = 10)

#Next button
next = Button(root, text = 'Next', command = read_email_from_gmail)
next.grid(row = 4, column = 1, pady = 20)



root.mainloop()

