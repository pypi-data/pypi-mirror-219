import logging as log
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def alert_email(username,password,sender,subject,content,emails):
    try:
        if emails==0:
            pass
        else:
            for i in emails:
                msg = MIMEMultipart('mixed')
                recipient = i

                msg['Subject'] = subject
                msg['From'] = sender
                msg['To'] = recipient
                html_message = MIMEText(content, 'html')
                msg.attach(html_message)

                mailServer = smtplib.SMTP('mail.smtp2go.com', 2525)
                mailServer.ehlo()
                mailServer.starttls()
                mailServer.ehlo()
                mailServer.login(username, password)
                mailServer.sendmail(sender, recipient, msg.as_string())
                mailServer.close()
                
    except Exception as e:
        log.error(e)

def emails_check(user_email,notify_me,notify_email,users,username,password,sender,subject,content):
    try:
        if notify_me==True and notify_email==True:
            emails=[user_email]
            for k in range(len(users)):
                p_notify_email=users[k]['notify_email']
                if p_notify_email==True:
                    emails.append(users[k]['user_email'])
                else:
                    emails=[user_email]
        elif notify_me==False:
            emails=[]
            for k in range(len(users)):
                p_notify_email=users[k]['notify_email']
                if p_notify_email==True:
                    emails.append(users[k]['user_email'])
                else:
                    emails=0
        
        alert_email(username,password,sender,subject,content,emails)
    except Exception as e:
        log.error(e)
        
