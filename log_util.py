# coding: utf-8
import logging

logfile = "result.log"
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s  %(pathname)s line:%(lineno)d  %(levelname)s : %(message)s thread:%(thread)d',
                    datefmt=' %Y-%m-%d %H:%M:%S',
                    filename='result.log',
                    filemode='a')


def get_log():
    return logging
