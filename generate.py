# coding: utf-8
from Crypto import Random, Hash
from Crypto.PublicKey import RSA
from io import BytesIO
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher
import Crypto.Signature.PKCS1_v1_5 as sign_PKCS1_v1_5
import base64
import aes_util
import zipfile
import zlib
import os
import gzip
import shutil
import  config
import  log_util
import sftp_util
import datetime
import write_excel
import send_email

logger = log_util.get_log()
time_now = datetime.datetime.now()
def generate_rsa():
    random_generator = Random.new().read
    rsa = RSA.generate(2048, random_generator)
 
    private_key = rsa.exportKey()
    with open("private_a.rsa", 'wb') as f:
        f.write(private_key)
 
    public_key = rsa.publickey().exportKey()
    with open("public_a.rsa", 'wb') as f:
        f.write(public_key)
def encrypt_content(pubkey,message):
    with open(pubkey) as f:
        key = f.read()
        pub_key = RSA.importKey(str(key))
        cipher = PKCS1_cipher.new(pub_key)
        encrypt_text = cipher.encrypt(bytes(message.encode("utf8")))
        
        rsa_text = base64.b64encode(encrypt_text)
        print(rsa_text  )
        text = rsa_text.decode('utf-8')
        print(text  )
    return text
def decrypt_msg(prikey,encrypt_txt):
    #使用私钥对内容进行rsa解密
    with open(prikey) as f:
        key = f.read()
        pri_key = RSA.importKey(key)
        cipher = PKCS1_cipher.new(pri_key)
        back_text = cipher.decrypt(base64.b64decode(encrypt_txt), 0)
        #print(back_text)
        print(back_text.decode('utf-8'))

def encrypt_msg_byte(public_key_third, byte_msg):
    pub_key = RSA.importKey(str(public_key_third))
    cipher = PKCS1_cipher.new(pub_key)
    encrypt_text = cipher.encrypt(byte_msg)
    return encrypt_text
def decrypt_msg_byte(private_key_self, byte_encrypt_txt):
    pri_key = RSA.importKey(private_key_self)
    cipher = PKCS1_cipher.new(pri_key)
    back_text = cipher.decrypt( byte_encrypt_txt, 0)
    return back_text
# 验签
def verify_sign(public_key_third, byte_msg, byte_sign):
    pubKey = RSA.importKey(public_key_third)
    # pubKey = RSA.importKey(publicKey)
    #h = MD5.new(data.encode('utf-8'))
    verifier = sign_PKCS1_v1_5.new(pubKey)
    _rand_hash = Hash.SHA256.new()
    _rand_hash.update(byte_msg)
    verify_ret = verifier.verify(_rand_hash, byte_sign)

    return verify_ret
# 签名
def sign_msg(private_key_self, byte_msg):
    signer_pri_obj = sign_PKCS1_v1_5.new(RSA.importKey(private_key_self))
    rand_hash = Hash.SHA256.new()
    rand_hash.update(byte_msg)
    signature = signer_pri_obj.sign(rand_hash)
    return signature
def bytes_to_int(bytes_key):
    return int.from_bytes(bytes_key, byteorder='big', signed=True)
def int_to_bytes(int_key):
    return int.to_bytes(int_key,length=2 , byteorder='big', signed=True)
def read_file(file_path, target_file):
    logger.info('开始解密文件: %s' % file_path)
    f = open(file_path, 'rb')
    try :

        aeskey_len = f.read(2)
        aeskey_len = bytes_to_int(aeskey_len)
        bytesA = f.read(aeskey_len)
        sign_len = f.read(2)
        sign_len = bytes_to_int(sign_len)
        bytesB = f.read(sign_len)
        file_tmp = f.read()
        aeskey = decrypt_msg_byte(config.private_key_self, bytesA)
        ziparr = aes_util.decrypt_text(aeskey, file_tmp)
        fio = BytesIO(ziparr)
        myzip = zipfile.ZipFile(file=fio)
        #print(myzip.namelist())
        text = myzip.read(myzip.namelist()[0]);
        content=text.decode("utf-8")
        #print(content)
        verify_sign_val = verify_sign(config.public_key_third,content.encode('UTF-8') ,bytesB )
        if verify_sign_val:
            target = open(target_file, 'w', encoding='utf-8')
            target.write(content)
            logger.info('签名验签通过')
            return content
        logger.info('签名验签不通过')
        return ''
        #print(verify_sign_val)
    finally:
        f.close()
def encypt_file(file_path,target_file):
    f = open(file_path, 'rb')
    logger.info('开始加密文件: %s' % file_path)
    target_dat = open(target_file, 'wb')
    try:
        byte_source = f.read()
        zip_bytes = BytesIO()
        myzip = zipfile.ZipFile(file=zip_bytes, mode='a',compression=zipfile.ZIP_DEFLATED)
        myzip.writestr(file_path,byte_source)
        myzip.close()
        byte_zip = zip_bytes.getvalue()
        random_key = Random.new().read(16)
        data_encrypt = aes_util.encrypt_text(random_key, byte_zip);
        byte_key = encrypt_msg_byte(config.public_key_third, random_key)
        byte_sign = sign_msg(config.private_key_self, byte_source)
        target_dat.write(int_to_bytes(len(byte_key)))
        target_dat.write(byte_key)
        target_dat.write(int_to_bytes(len(byte_sign)))
        target_dat.write(byte_sign)
        target_dat.write(data_encrypt)
    finally:
        f.close()
        target_dat.close()
def file_info():
    path = os.path.join(os.getcwd(), "dest.zip")
    zip_file = zipfile.ZipFile(path)
    for names in zip_file.namelist():
        print(zip_file.extract(names))
def file_write(file_path):
    f = open(file_path, 'wb')
    try:
        a = 128
        b = 256
        f.write(int_to_bytes(a))
        f.write(int_to_bytes(b))

    finally:
        f.close()
def file_read(file_path):
    f = open(file_path, 'rb')
    try:
        key = f.read(2)
        print(bytes_to_int(key))
        key = f.read(2)
        print(bytes_to_int(key))

    finally:
        f.close()
def get_time_str(format):
    return time_now.strftime(format)
def get_folder(folder):

    # %Y-%m-%d %H:%M:%S
    year = get_time_str('%Y')
    month = get_time_str('%m')
    day = get_time_str('%d')
    path = '''/in/%s/%s/%s/%s/1/''' % (folder, year, month, day)
    return path
def get_file_name(prefix,today, count):
    file_name = '''%s_log%s_%d.zip''' % (prefix, today, count)
    return file_name
def download_file(folder,  prefix, today, count):
    path = get_folder(folder)

    file_name = get_file_name(prefix, today, count)
    full_path = path + file_name
    sftp_util.download_file(file_name, full_path)
    return file_name


def download_all_file(today ):
    sftp_client = sftp_util.get_sftp_client()
    try:
        download_all_file_tree(sftp_client, today, '10')
        download_all_file_tree(sftp_client, today, '40')
        download_all_file_tree(sftp_client, today, '50')
    except FileNotFoundError as e:
        return False
    finally:
        sftp_util.close_sftp_client(sftp_client)
    return True

def download_all_file_tree(sfp_client, today, folder):
    if not os.path.exists(today):
        os.makedirs(today)
    remote_dir = get_folder(folder)
    for file in sftp_util.list_dirs(sfp_client, remote_dir):
        local_path = os.path.join(today, file)
        remote_path = os.path.join(remote_dir, file)
        if  os.path.splitext(remote_path)[1] == '.zip':
            sftp_util.download_file(sfp_client, local_path, remote_path)


def decrypt_all_file(today):
    for file in os.listdir(today):
        file_arr = file.split('.')
        prefix = file_arr[0]
        prefix = 'decrypt_' + prefix + '.txt'
        read_file(os.path.join(today, file), os.path.join(today, prefix))


def analysis_file(today):
    for file in os.listdir(today):
        if  file.startswith('decrypt'):
            if 'custinf' in file:
                write_excel.read_custinf_txt_file(os.path.join(today, file))
            elif 'overdue' in file:
                write_excel.read_overdue_txt_file(os.path.join(today, file))
            else:
                write_excel.read_tradinf_txt_file(os.path.join(today, file))

def encrypt_excel(today):
    write_excel.encrypt_excel(today)

def delete_not_encrypt_file(today):
    for file in os.listdir(today):
        if file.endswith('.txt') or file.startswith('excel_decrypt'):
            os.remove(os.path.join(today, file))

def main():
    today = get_time_str('%Y%m%d')
    logger.info('开始处理%s文件' % today)
    # 下载文件
    logger.info('开始从sftp下载文件')
    down_ok = download_all_file(today)
    if not down_ok:
        logger.info('下载文件失败')
        return 0
    # 解密文件
    logger.info('开始解密下载文件')
    decrypt_all_file(today)
    # 解析文件
    logger.info('开始解析文件成excel')
    analysis_file(today)
    # 加密excel文件
    logger.info('开始加密解析好excel')
    encrypt_excel(today)
    # 删除非加密文件
    logger.info('开始删除非加密文件')
    delete_not_encrypt_file(today)
    logger.info('开始发送邮件')
    send_email.send(today)


if __name__=="__main__":
    main()

