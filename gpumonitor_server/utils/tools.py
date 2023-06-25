import datetime

import paramiko
from flask import jsonify


def detect_gpu_status(host, user, passwd, timeout=3):
    ssh = paramiko.SSHClient()
    key = paramiko.AutoAddPolicy()
    ssh.set_missing_host_key_policy(key)
    try:
        ssh.connect(host, 22, user, passwd)
    except:
        return 0, []
    stdin, stdout, stderr = ssh.exec_command('ps -aux')
    process_dict = {}
    for i in stdout.readlines():
        items = i.split()
        user = items[0]
        des = ' '.join(items[10:])
        process_dict[items[1]] = (user, des)
    stdin, stdout, stderr = ssh.exec_command('nvidia-smi')
    state = []
    for i in stdout.readlines():
        items = i.split()
        if len(items) == 7 and '.' not in items[2] and 'MiB' in items[5]:
            gpu_id, pid, _, desc_simple, pmem = items[1:6]
            dic = {
                'user': process_dict[pid][0], 'gpuid': gpu_id, 'pid': pid, 'desc': process_dict[pid][1], 'mem': pmem
            }
            state.append(dic)
    ssh.close()
    return 1, state


def get_pro_time(host, user, passwd, pid):
    ssh = paramiko.SSHClient()
    key = paramiko.AutoAddPolicy()
    ssh.set_missing_host_key_policy(key)
    try:
        ssh.connect(host, 22, user, passwd)
    except:
        return 0, []
    # 进程运行时间
    _, stdout, _ = ssh.exec_command('ps -o lstart,etime -p ' + str(pid))
    start_time, duration = 0, 0
    for line in stdout:
        items = line.split()
        if items[0] == 'STARTED':
            continue
        start_time = ':'.join(items[:5])
        duration = str(items[5]).replace('\n', '')
    start_time = datetime.datetime.strptime(start_time, "%a:%b:%d:%H:%M:%S:%Y")
    return start_time, duration


def run_mc_server(host, user, passwd):
    ssh = paramiko.SSHClient()
    key = paramiko.AutoAddPolicy()
    ssh.set_missing_host_key_policy(key)
    ssh.connect(host, 22, user, passwd)
    _, stdout, _ = ssh.exec_command(
        'cd /opt/mc/paper/ && screen -dmS minecraft java -Xms2048m -Xmx4096m -jar paper118.jar nogui > minecraft.log 2>&1\n')
    return jsonify({"code": 200, "message": "mc-server : 启动成功!"})


def stop_mc_server(host, user, passwd):
    ssh = paramiko.SSHClient()
    key = paramiko.AutoAddPolicy()
    ssh.set_missing_host_key_policy(key)
    ssh.connect(host, 22, user, passwd)
    _, stdout, _ = ssh.exec_command('cd /opt/mc/paper/ && screen -S minecraft -p 0 -X stuff "stop^M"\n')
    return jsonify({"code": 200, "message": "mc-server : 关闭成功!"})


def get_log(host, user, passwd, command):
    ssh = paramiko.SSHClient()
    key = paramiko.AutoAddPolicy()
    ssh.set_missing_host_key_policy(key)
    try:
        ssh.connect(host, 22, user, passwd)
    except:
        return 0, []
    # 进程运行时间
    _, stdout, _ = ssh.exec_command(command)
    log = stdout.readlines()
    cur_log = ''.join(log)
    return cur_log


if __name__ == "__main__":
    # a = detect_gpu_status('219.216.64.175', 'maqi', '.')
    # b = get_pro_time('202.199.6.23', 'maqi', '.', 13677)
    # a = detect_gpu_status('219.216.64.175', 'gpu_monitor', 'neu.')
    c = get_log('219.216.64.204', 'gpu_monitor', 'neu.', "tail -100 /data0/maqi/BELLE/train/log.log")

    # e = run_mc_server('219.216.64.204', 'mc', 'mc')
    # f = stop_mc_server('219.216.64.204', 'mc', 'mc')
    print()
