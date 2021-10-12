# coding: utf-8
import config
import paramiko
import log_util

logger = log_util.get_log()


def get_sftp_client():
    t = paramiko.Transport((config.sftp_ip, config.sftp_port))
    t.banner_timeout = 10
    t.connect(username=config.sftp_user, password=config.sftp_pwd)
    sftp = paramiko.SFTPClient.from_transport(t)
    return sftp


def sftp_upload_file(sftp_client, remote_path, local_path):
    try:
        sftp_client.put(local_path, remote_path)
        return True
    except Exception as e:
        logger.error(e)
        return False


def sftp_down_file(sftp_client, remote_path, local_path):
    try:
        sftp_client.get(remote_path, local_path)
        return True
    except Exception as e:
        logger.error(e)
        return False


def close_sftp_client(sfp_client):
    sfp_client.close()


def download_file(sftp_client, local_path, remote_path):
    return sftp_down_file(sftp_client, remote_path, local_path)


def upload_file(sftp_client, local_path, remote_path):
    return sftp_upload_file(sftp_client, remote_path, local_path)


def list_dirs(sftp_client, remote_dir):
    return sftp_client.listdir(remote_dir)


if __name__ == '__main__':
    # download_file('download.log', '/root/result.log')
    upload_file('test3.txt', '/root/test3.txt')
