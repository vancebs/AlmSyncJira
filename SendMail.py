# -*- coding: UTF-8 –*-
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import threading

def send_email_by_smtp(subject,message,receiveMail):
    sender_email_address = "service.jira@t2mobile.com"  # 用于发送邮件的邮箱的密码。修改成自己的邮箱的密码
    sender_email_password = "bBDCP5ZKQ72QUzcP"  # 用于发送邮件的邮箱的smtp服务器，也可以直接是IP地址  # 修改成自己邮箱的sntp服务器地址；qq邮箱不需要修改此值
    smtp_server_host = "smtphz.qiye.163.com"# 修改成自己邮箱的sntp服务器监听的端口；qq邮箱不需要修改此值
    smtp_server_port = 465 # 要发往的邮箱

    receiver_email = receiveMail # 接收者
    message_subject = subject # 要发送的邮件主题
    message_context = message # 要发送的邮件内容

    # 邮件对象，用于构建邮件
    message = MIMEText(message_context, 'plain', 'utf-8') # 设置发件人（声称的）
    message["From"] = Header(sender_email_address, "utf-8") # 设置收件人（声称的）
    message["To"] = Header(receiver_email, "utf-8") # 设置邮件主题
    message["Subject"] = Header(message_subject, "utf-8")

    # 连接smtp服务器。如果没有使用SSL，将SMTP_SSL()改成SMTP()即可其他都不需要做改动
    email_client = smtplib.SMTP_SSL(smtp_server_host, smtp_server_port)
    try:
        # 验证邮箱及密码是否正确
        email_client.login(sender_email_address, sender_email_password)
        print("smtp----login success, now will send an email to {receiver_email}")
    except:
        print("smtp----sorry, username or password not correct or another problem occur")
    else:
        # 发送邮件
        email_client.sendmail(sender_email_address, receiver_email, message.as_string())
        print("smtp----send email to {receiver_email} finish")
    finally:
        # 关闭连接
        email_client.close()
