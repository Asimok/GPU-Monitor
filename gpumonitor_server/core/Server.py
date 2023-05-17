import datetime
import threading
import time
from typing import List

import paramiko

from config.setting import REFRESH_SEC, UPDATE_GAP
from core.GPU import GPU
from core.Program import Program
from core.ProgramLogger import ProgramLogger


class Server(threading.Thread):
    def __init__(self, server_name: str, ip: str, username: str, password: str):
        super().__init__()
        self.LOGGER = ProgramLogger()
        self.server_name = server_name
        self.ip = ip
        self.username = username
        self.password = password

        self.gpu_list: List[GPU] = []

        self.ssh: paramiko.SSHClient = None
        # 线程相关
        self.update_time = datetime.datetime.timestamp(datetime.datetime.now())  # 更新时间
        self.paused = False
        self.start()

    def check(self):
        if datetime.datetime.timestamp(datetime.datetime.now()) - self.update_time > UPDATE_GAP:
            self.pause()
            return True
        return False

    def run(self) -> None:
        while True:
            if not self.paused and not self.check():
                try:
                    self.update_state()
                except:
                    if not self.update_ssh():
                        self.gpu_list = []
            time.sleep(REFRESH_SEC)

    def resume(self):
        print("notify thread: ", self.server_name)
        self.paused = False

    def pause(self):
        print("thread sleep: ", self.server_name)
        self.paused = True

    def notify_thread(self):
        if self.paused:
            # 如果线程没有启动，启动线程
            self.resume()

    def json(self):
        return {
            'server_name': self.server_name,
            'gpu_list': [gpu.json() for gpu in self.gpu_list],
        }

    def update_ssh(self):
        ssh = paramiko.SSHClient()
        key = paramiko.AutoAddPolicy()
        ssh.set_missing_host_key_policy(key)
        try:
            ssh.connect(self.ip, 22, self.username, self.password)
        except:
            return False
        self.ssh = ssh
        return True

    def get_pro_time(self, pid):
        # 进程运行时间
        _, stdout, _ = self.ssh.exec_command('ps -o lstart,etime -p ' + pid)
        start_time, duration = 0, 0
        for line in stdout:
            items = line.split()
            if items[0] == 'STARTED':
                continue
            start_time = ':'.join(items[:5])
            duration = str(items[5]).replace('\n', '')
        start_time = datetime.datetime.strptime(start_time, "%a:%b:%d:%H:%M:%S:%Y")
        return str(start_time), duration

    def get_log(self, pid):
        # 获取日志
        cmd = self.LOGGER.get_log(pid)
        _, stdout, _ = self.ssh.exec_command(cmd)
        log = stdout.readlines()
        cur_log = ''.join(log)
        cur_log = cur_log.replace('\n', '<br>').replace('\r', '<br>')
        return cur_log[-2000:]

    def update_state(self):
        # 进程状态
        _, stdout, _ = self.ssh.exec_command('ps -o ruser=userForLongName -e -o pid,cmd')
        process_dict = {}
        for line in stdout:
            items = line.split()
            pid = items[0]
            des = ' '.join(items[2:])
            process_dict[items[1]] = (pid, des)
        # GPU 状态
        _, stdout, _ = self.ssh.exec_command(
            'nvidia-smi --query-gpu=index,memory.used,memory.total,temperature.gpu,fan.speed,power.draw --format=csv,noheader')
        gpu_list = []
        for line in stdout:
            num, use_memory, total_memory, temp, fan, pwr = map(str.strip, line.split(','))
            if str(use_memory).__contains__("MiB"):
                use_memory = int(use_memory[:-3])
            if str(total_memory).__contains__("MiB"):
                total_memory = int(total_memory[:-3])
            gpu_list.append(GPU(num, use_memory, total_memory, temp, fan, pwr, []))
        # GPU 程序
        for gpu in gpu_list:
            _, stdout, _ = self.ssh.exec_command(
                f'nvidia-smi -i {gpu.num} --query-compute-apps=pid,used_memory --format=csv,noheader')
            for line in stdout:
                pid, use_memory = map(str.strip, line.split(','))
                # 删除不存在的pid
                cur_log = ''
                log_cmd = '请先绑定日志!'
                try:
                    if self.LOGGER.get_log(pid):
                        # 获取日志
                        cur_log = self.get_log(pid)
                        log_cmd = self.LOGGER.get_log(pid)
                except:
                    pass
                username, command = process_dict[pid]
                if use_memory.__contains__("MiB"):
                    use_memory = int(use_memory[:-3])
                start_time, duration = self.get_pro_time(pid)
                gpu.program_list.append(
                    Program(pid, command, username, use_memory, start_time, duration, cur_log, log_cmd))

        self.gpu_list = gpu_list
