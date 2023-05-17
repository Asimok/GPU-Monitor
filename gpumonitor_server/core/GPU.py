from typing import List

from core.Program import Program


class GPU:

    def __init__(self, num, use_memory, total_memory, temp, fan, pwr, program_list):
        self.num = num
        self.fan = fan
        self.temp = temp
        self.pwr = pwr
        self.use_memory = use_memory
        self.total_memory = total_memory
        self.program_list: List[Program] = program_list

    def json(self):
        return {
            'num': self.num,
            'fan': self.fan,
            'temp': self.temp,
            'pwr': self.pwr,
            'use_memory': self.use_memory,
            'total_memory': self.total_memory,
            'program_list': [program.json() for program in self.program_list]
        }