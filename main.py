import smtplib
import time
import imaplib
import email


ORG_EMAIL   = "@gmail.com" 
FROM_EMAIL = raw_input("Enter your email: ")
FROM_PWD    = raw_input("Enter your password: ")
SMTP_SERVER = "imap.gmail.com"
SMTP_PORT   = 993

def read_email_from_gmail():
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

read_email_from_gmail()