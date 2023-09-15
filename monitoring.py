import smtplib
from email.header import Header
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os
import time

def mail_sender(file_path, line):
    smtp = smtplib.SMTP('smtp.naver.com', 587)
    smtp.ehlo()
    smtp.starttls()

    smtp.login("hsy15789@naver.com","xhfl159!!")

    myemail = "hsy15789@naver.com"
    youremail = "hsy15789@naver.com"

    subject = f"Detect Suspected Files {file_path}"
    message = f"Detect Suspected Files {file_path}:{line}"

    msg = MIMEText(message.encode('utf-8'), _subtype='plain', _charset='utf-8')
    msg['Subject'] = Header(subject.encode('utf-8'), 'utf-8')
    msg['From'] = myemail
    msg['To'] = youremail
    smtp.sendmail(myemail,youremail,msg.as_string())
    smtp.quit()

#모니터링　코드
DIR_WATCH = "static"
previous_files = set(os.listdir(DIR_WATCH))

while True:
    time.sleep(1)
    print("Monitoring")
    current_files = set(os.listdir(DIR_WATCH))
    new_files = current_files - previous_files
    for file in new_files:
        if file.endswith('.php') or file.endswith('.html'):
            print(f"New File : {file}")
            file_path = os.path.join(DIR_WATCH, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                for line in lines:
                    if line.startswith("#") or line.startswith("//"):
                        print(f"Comment processing {line}")
                        mail_sender(file_path, line)

    previous_files = current_files