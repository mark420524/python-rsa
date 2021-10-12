# --------------------------------------
# - -*- coding:utf-8 -*-               -
# - Author : L                         -
# --------------------------------------


import smtplib
import os
import datetime
# email 用于构建邮件内容
from email.header import Header
# 发送附件
from email.mime.application import MIMEApplication
# 发送多个部分
from email.mime.multipart import MIMEMultipart
# 专门发送文本的！MIMEText
from email.mime.text import MIMEText
import log_util
import config

logger = log_util.get_log()

def send(today):
    logger.info("  send_email   working......")
    # 邮件标题title
    title = "拨打数据邮件"
    # 附件路径 都可以
    # file_path = get_file()
    # 邮件正文内容
    time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    text = "尊敬的各位领导: \n" \
           "    附件为%s拨打数据 \n" \
           "    注:发送时间%s！如需改时间请联系IT人员" % (today, today, today, today,  time_now)

    # # 邮箱正文内容，第一个参数为内容，第二个参数为格式(plain 为纯文本)，第三个参数为编码
    # msg = MIMEText(msg, 'plain', 'utf-8')
    # 构建邮件体
    msg = MIMEMultipart()
    msg['From'] = config.from_addr
    msg['To'] = ','.join(config.to_addr)
    msg['Subject'] = Header(title, 'utf-8')
    # 构建正文
    part_text = MIMEText(text)
    msg.attach(part_text)
    for file in os.listdir(today):
        if file.startswith('excel_encrypt'):
            # 构建邮件附件
            part_attach = MIMEApplication(open(os.path.join(today, file), 'rb').read())  # 打开附件
            filename = file
            part_attach.add_header('Content-Disposition', 'attachment', filename=filename)  # 为附件命名
            msg.attach(part_attach)  # 添加附件

    # 开启发信服务，这里使用的是加密传输
    # server = smtplib.SMTP_SSL()
    server = smtplib.SMTP_SSL(host=config.smtp_server)
    server.connect(config.smtp_server, config.smtp_port)
    try:
        # 登录发信邮箱5
        server.login(config.from_addr, config.smtp_password)
        # 发送邮件
        server.sendmail(config.from_addr, config.to_addr, msg.as_string())
        logger.info("邮件发送成功,发件人:%s 收件人:%s " % (config.from_addr, config.to_addr))
    except Exception as err:
        logger.info("邮件发送失败：%s" % (err))
        exit()
    finally:
        # 关闭服务器
        server.quit()
