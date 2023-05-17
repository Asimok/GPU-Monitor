class Program:
    def __init__(self, pid, command, username, use_memory, start_time, duration, cur_log, log_cmd):
        self.pid = pid
        self.command = command
        self.username = username
        self.use_memory = use_memory
        self.start_time = start_time
        self.duration = duration
        self.cur_log = cur_log
        self.log_cmd = log_cmd

    def json(self):
        return self.__dict__
