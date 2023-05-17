class ProgramLogger:
    def __init__(self):
        self.log_dict = {}

    # 新增日志
    def add_log(self, pid, cmd):
        self.log_dict[pid] = cmd

    # 更新日志
    def update_log(self, pid, cmd):
        self.log_dict[pid] = cmd

    # 删除日志
    def del_log(self, pid):
        self.log_dict.pop(pid)

    # 获取日志
    def get_log(self, pid):
        return self.log_dict[pid]