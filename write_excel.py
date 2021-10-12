# coding: utf-8
import pandas as pd
from pandas import ExcelWriter
import os
import jpype
import config



def format_custinf_list(file_path):
    result = {}
    rcus_custid = []
    rcus_name = []
    rcus_principal = []
    rcus_bal = []
    rcus_full_repay_amt = []
    typ_name = []
    rloan_retuday = []
    created_time = []
    rcus_warning_lev = []
    rcus_overdue_p = []
    rcus_mobile = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            line_array = line.strip().split('|$|')
            rcus_custid.append(line_array[0])
            rcus_name.append(line_array[1])
            rcus_principal.append(line_array[2])
            rcus_bal.append(line_array[3])
            rcus_full_repay_amt.append(line_array[4])
            typ_name.append(line_array[5])
            rloan_retuday.append(line_array[6])
            created_time.append(line_array[7])
            rcus_warning_lev.append(line_array[8])
            rcus_overdue_p.append(line_array[9])
            rcus_mobile.append(line_array[10])
    result['客户编号'] = rcus_custid
    result['客户姓名'] = rcus_name
    result['全部贷款本金'] = rcus_principal
    result['全部剩余本金'] = rcus_bal
    result['提前结清金额'] = rcus_full_repay_amt
    result['催收状态'] = typ_name
    result['最近还款日'] = rloan_retuday
    result['最近催记时间'] = created_time
    result['预警优先级'] = rcus_warning_lev
    result['违约概率'] = rcus_overdue_p
    result['授信手机号'] = rcus_mobile
    return result


def format_overdue_list(file_path):
    result = {}
    loan_Id = []
    rpmt_cust_id = []
    rlor_bal = []
    rlor_created_time = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            line_array = line.strip().split('|$|')
            loan_Id.append(line_array[0])
            rpmt_cust_id.append(line_array[1])
            rlor_bal.append(line_array[2])
            rlor_created_time.append(line_array[3])
    result['贷款编号'] = loan_Id
    result['客户编号'] = rpmt_cust_id
    result['入催时剩余本金'] = rlor_bal
    result['入催时间'] = rlor_created_time
    return result


def format_tradinf_list(file_path):
    result = {}
    rpmt_cust_id = []
    rcus_name = []
    rpmt_acct_seq = []
    rcus_warning_lev = []
    rloan_retuday = []
    rloan_tcapi = []
    rloan_bal = []
    rloan_overinte = []
    rloan_overpenf = []
    rloan_overfee = []
    rloan_stotal = []
    rloan_warning_date = []

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            line_array = line.strip().split('|$|')
            rpmt_cust_id.append(line_array[0])
            rcus_name.append(line_array[1])
            rpmt_acct_seq.append(line_array[2])
            rcus_warning_lev.append(line_array[3])
            rloan_retuday.append(line_array[4])
            rloan_tcapi.append(line_array[5])
            rloan_bal.append(line_array[6])
            rloan_overinte.append(line_array[7])
            rloan_overpenf.append(line_array[8])
            rloan_overfee.append(line_array[9])
            rloan_stotal.append(line_array[10])
            rloan_warning_date.append(line_array[11])
    result['客户编号'] = rpmt_cust_id
    result['客户姓名'] = rcus_name
    result['贷款编号'] = rpmt_acct_seq
    result['客户预警等级'] = rcus_warning_lev
    result['最近应还日'] = rloan_retuday
    result['贷款本金'] = rloan_tcapi
    result['剩余本金'] = rloan_bal
    result['剩余利息'] = rloan_overinte
    result['剩余罚息'] = rloan_overpenf
    result['剩余费用'] = rloan_overfee
    result['应还总额'] = rloan_stotal
    result['预警日期'] = rloan_warning_date
    return result

def get_target_file_name(file_path):
    file_folder = file_path[0:8]

    file_name = file_path[9:]
    target_file = 'excel_' + file_name.split('.')[0] + '.xlsx'
    return os.path.join(file_folder, target_file)


def write_custinf_excel(file_path, list):
    columns = ['客户编号', '客户姓名', '全部贷款本金', '全部剩余本金', '提前结清金额', '催收状态', '最近还款日', '最近催记时间', '预警优先级', '违约概率', '授信手机号']
    pf = format_df(list, columns)
    target_file = get_target_file_name(file_path)
    write__excel(pf, target_file)


def write_overdue_excel(file_path, list):
    columns = ['贷款编号', '客户编号', '入催时剩余本金', '入催时间']
    pf = format_df(list, columns)
    target_file = get_target_file_name(file_path)
    write__excel(pf, target_file)

def write_tradinf_excel(file_path, list):
    columns = ['客户编号','客户姓名','贷款编号','客户预警等级','最近应还日','贷款本金','剩余本金','剩余利息','剩余罚息','剩余费用','应还总额','预警日期']
    pf = format_df(list, columns)
    target_file = get_target_file_name(file_path)
    write__excel(pf, target_file)


def format_df(list, columns):
    pf = pd.DataFrame(list, columns=columns)
    return pf


def write__excel(pf, target_file):
    with ExcelWriter(target_file) as writer:
        pf.to_excel(writer, index=False)


def read_custinf_txt_file(file_path):
    list = format_custinf_list(file_path)
    write_custinf_excel(file_path, list)


def read_overdue_txt_file(file_path):
    list = format_overdue_list(file_path)
    write_overdue_excel(file_path, list)


def read_tradinf_txt_file(file_path):
    list = format_tradinf_list(file_path)
    write_tradinf_excel(file_path, list)



def start_jvm():
    project_dir = os.path.dirname(os.path.abspath(__file__))
    jvm_path = jpype.getDefaultJVMPath()
    # 这里根据实际的jxcell.jar路径进行配置,我这里的放的位置是本文件同级目录的lib/jxcell.jar

    jxcell_path = os.path.join(project_dir, 'lib/')
    if not jpype.isJVMStarted():
        jpype.startJVM(jvm_path, '-ea', '-Djava.ext.dirs=' + jxcell_path, convertStrings=False)
    return jpype


def encrypt(jpype, source, target, passwd):
    encrypt_excel = jpype.JClass('com.silivall.excel.ExcelOperator')
    m_view = encrypt_excel()
    m_view.encryptExcelFile(source, target, passwd)


def encrypt_excel(today):
    for file in os.listdir(today):
        if file.startswith('excel_decrypt'):
            target_file = file.replace('excel_decrypt', 'excel_encrypt')
            jpype_vm = start_jvm()
            encrypt(jpype_vm, os.path.join(today, file), os.path.join(today, target_file), config.excel_passwd)
