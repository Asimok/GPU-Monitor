import datetime

import paramiko
from flask import jsonify

from core.GPU import GPU
from core.Program import Program


def detect_gpu_status(host, user, passwd, timeout=3):
    ssh = paramiko.SSHClient()
    key = paramiko.AutoAddPolicy()
    ssh.set_missing_host_key_policy(key)

    ssh.connect(host, 22, user, passwd)

    _, stdout, _ = ssh.exec_command('ps -o ruser=userForLongName -e -o pid,cmd')
    process_dict = {}
    for line in stdout:
        items = line.split()
        pid = items[0]
        des = ' '.join(items[2:])
        process_dict[items[1]] = (pid, des)
    # GPU 状态
    _, stdout, _ = ssh.exec_command(
        'nvidia-smi --query-gpu=index,memory.used,memory.total,temperature.gpu,fan.speed,power.draw --format=csv,noheader')
    gpu_list = []
    for line in stdout:
        num, use_memory, total_memory, temp, fan, pwr = map(str.strip, line.split(','))
        if str(use_memory).__contains__("MiB"):
            use_memory = int(use_memory[:-3])
        if str(total_memory).__contains__("MiB"):
            total_memory = int(total_memory[:-3])
        gpu_list.append(GPU(num, use_memory, total_memory, temp, fan, pwr, []))

    # # GPU 程序
    for gpu in gpu_list:
        _, stdout, _ = ssh.exec_command(
            f'nvidia-smi -i {gpu.num} --query-compute-apps=pid,used_memory --format=csv,noheader')
        for line in stdout:
            pid, use_memory = map(str.strip, line.split(','))
            # 删除不存在的pid
            cur_log = ''
            log_cmd = '请先绑定日志!'
            try:
                username, command = process_dict[pid]
                if use_memory.__contains__("MiB"):
                    use_memory = int(use_memory[:-3])
                start_time, duration = 1, 1
                gpu.program_list.append(
                    Program(pid, command, username, use_memory, start_time, duration, cur_log, log_cmd))
            except Exception as e:
                print(str(e))

    ssh.close()
    return 1


def get_pro_time(host, user, passwd, pid):
    ssh = paramiko.SSHClient()
    key = paramiko.AutoAddPolicy()
    ssh.set_missing_host_key_policy(key)
    try:
        ssh.connect(host, 22, user, passwd)
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
    except Exception as e:
        print(str(e))
        return 0, []


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
        # 进程运行时间
        _, stdout, _ = ssh.exec_command(command)
        log = stdout.readlines()
        cur_log = ''.join(log)
        return cur_log

    except Exception as e:
        print(str(e))
        return 0, []


if __name__ == "__main__":
    # a = detect_gpu_status('219.216.64.175', 'maqi', '.')
    # b = get_pro_time('202.199.6.23', 'maqi', '.', 13677)
    a = detect_gpu_status('219.216.64.231', 'gpu_monitor', 'neu.')
    # c = get_log('219.216.64.231', 'gpu_monitor', 'neu.', "tail -100 /data0/maqi/BELLE/train/log.log")

    # e = run_mc_server('219.216.64.204', 'mc', 'mc')
    # f = stop_mc_server('219.216.64.204', 'mc', 'mc')
    print()
