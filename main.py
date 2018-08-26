import smtplib
import time
import imaplib
import email
from Tkinter import *


SMTP_SERVER = "imap.gmail.com"
SMTP_PORT   = 993
mail = imaplib.IMAP4_SSL(SMTP_SERVER)

root = Tk()
root.geometry('430x220')
root.title('Sign In')
root.configure(background = 'antique white')

def checking(event):
    if email == root.focus_get():
        error.configure(text = 'Checking email...', fg = 'blue')
    elif password == root.focus_get():
        error.configure(text = 'Checking password...', fg = 'blue')

def login_success():
    mail.login(email.get(),password.get())
    print "login success"

def login_error():
    error.configure(text = 'Email or password is incorrect', fg = 'red')
    time.sleep(5)
    print "login error"
    time.sleep(5)
    email.delete(0, END)
    password.delete(0, END)

def login(*event):
    try:
        login_success()
        root.destroy()
        read_email_from_gmail()

    except:
        login_error()

def read_email_from_gmail():
    try:
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
                    print "success 6"
                    msg = email.message_from_string(response_part[1])
                    print "success 7"
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

#Email icon
icon = PhotoImage(file = 'Email_icon.gif')
email_icon = Label(root, image= icon, justify = LEFT)
email_icon.grid(column = 1)

#Entry for email address and password
Label(root, text = "Email-address", justify = LEFT, bg = 'antique white').grid(row=2, padx = 10, pady = 10)
Label(root, text = "Password", justify = LEFT, bg = 'antique white').grid(row=3, padx = 10)

email = Entry(root, justify = LEFT, width = 35)
password = Entry(root, justify = LEFT, show = '*', width = 35)
email.grid(row=2, column=1, padx = 10, pady = 10)
password.grid(row=3, column=1, padx = 10)
email.index(END)
password.index(END)

#For error part
error = Label(root, text = 'Have a great day ahead', justify = LEFT, font = ('Helvetica',10), bg = 'antique white')
error.grid(row = 4, column = 1, padx = 10)

email.bind("<FocusIn>", checking)
password.bind("<FocusIn>", checking)

#Next button
next = Button(root, text = 'Login', command = login, bg = 'blue', fg = 'white', bd = 0)
next.grid(row = 5, column = 1, pady = 20)
next.bind("<Return>", login)

root.mainloop()

