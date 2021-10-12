# coding: utf-8

'''
 配置文件,配置私钥公钥
 上线后需改为生产环境
'''

private_key_self = '''-----BEGIN RSA PRIVATE KEY-----
-----END RSA PRIVATE KEY-----'''

public_key_third = '''-----BEGIN PUBLIC KEY-----
-----END PUBLIC KEY-----'''

'''
 配置文件,配置sftp 
 上线后需改为生产环境
'''

sftp_user = ''
sftp_pwd = ''
sftp_ip = ''
sftp_port = 22

# excel 加密密码
excel_passwd = '$123Yy456'


'''
  发送邮箱配置
'''
# 发信方邮箱
from_addr = ''
smtp_password = ''
# 收信方邮箱
to_addr = ['' ]
# 发信服务器
smtp_server = 'smtp.exmail.qq.com'
smtp_port = 465
