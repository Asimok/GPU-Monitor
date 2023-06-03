import datetime
import random

from cffi.cparser import lock

from config.setting import COON, IP_UPDATE_TIME


class IpInfoDao:
    def __init__(self, coon):
        self.conn = coon
        self.c = self.conn.cursor()
        # 判断数据表 ip_info 是否存在 不存在则创建
        self.c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='ip_info'")
        result = self.c.fetchone()
        if result is not None:
            print("数据表 ip_info 已存在")
        else:
            print("数据表 ip_info 不存在,即将创建")
            self.c.execute(
                '''CREATE TABLE IF NOT EXISTS ip_info (ip TEXT, date DATE,times INTEGER,last_update DATE)''')

    # 插入ip访问记录
    def add_ip(self, ip, _cur_time):
        # cur_time = datetime.datetime.now()
        # print(_cur_time)
        try:
            lock.acquire(True)
            # 判断是否存在
            self.c.execute("SELECT times FROM ip_info WHERE ip = ? and date = ?", (ip, _cur_time))
            time = self.c.fetchone()
            # print("times", time)
            if time:
                # 限制 IP_UPDATE_TIME min 插入一次
                self.c.execute("SELECT last_update FROM ip_info WHERE ip = ? and date = ?", (ip, _cur_time))
                last_update = self.c.fetchone()
                # 判断时间间隔
                if (datetime.datetime.now() - datetime.datetime.strptime(last_update[0],
                                                                         '%Y-%m-%d %H:%M:%S.%f')).seconds / 60 >= IP_UPDATE_TIME:
                    # 插入数据
                    self.c.execute("UPDATE ip_info SET times = times + 1,last_update = ? WHERE ip = ? and date = ?",
                                   (datetime.datetime.now(), ip, _cur_time))
            else:
                self.c.execute("INSERT INTO ip_info (ip, date,times,last_update) VALUES (?,?,?,?)",
                               (ip, _cur_time, 1, datetime.datetime.now()))
            self.conn.commit()
        finally:
            lock.release()

    # 查询一个月内的数据
    def get_ip_data_one_month(self, _cur_time, gap=30):
        # 先计算一个月前的时间
        month_ago = _cur_time - datetime.timedelta(days=gap)
        # 执行查询语句
        _data = 0
        try:
            lock.acquire(True)
            self.c.execute("SELECT ip, date,times FROM ip_info WHERE date BETWEEN ? AND ?", (month_ago, _cur_time))
            _data = self.c.fetchall()
        finally:
            lock.release()
        return _data

    # 今日活跃用户
    # 本月活跃用户
    def get_ip_nums(self, _cur_time, gap=1):
        # 获取gap范围内的ip数量
        days_ago = _cur_time - datetime.timedelta(days=gap)
        # _data = 0
        ip_set = set()
        try:
            lock.acquire(True)
            # 需要对相同ip去重
            self.c.execute("SELECT ip FROM ip_info WHERE date BETWEEN ? AND ?", (days_ago, _cur_time))
            ip_data = self.c.fetchall()
            for ip in ip_data:
                ip_set.add(ip[0])
            # self.c.execute("SELECT COUNT(ip) FROM ip_info WHERE date BETWEEN ? AND ?", (days_ago, _cur_time))
            # _data = self.c.fetchone()
        finally:
            lock.release()
        return len(ip_set)

    # 历史点击量
    def get_ip_nums_all(self):
        _data = []
        try:
            lock.acquire(True)
            # self.c.execute("SELECT COUNT(ip) FROM ip_info")
            # _data = self.c.fetchone()
            # 查询总数据量
            self.c.execute("SELECT times FROM ip_info")
            ip_times = self.c.fetchall()
            # 累加 ip_times
            temp = []
            for times in ip_times:
                temp.append(times[0])
            _data.append(sum(temp))
        finally:
            lock.release()
        return _data[0]


if __name__ == '__main__':
    coon = COON
    ip_info_dao = IpInfoDao(coon)
    cur_time = datetime.datetime.now()
    # 生成2023-4-10 到 2023-5-17 的数据
    # for i in range(20):
    #     one_month_ago = cur_time - datetime.timedelta(days=i)
    #     for i in range(random.randint(1, 9)):
    #         ip_info_dao.add_ip("192.168.3." + str(i), one_month_ago.strftime("%Y-%m-%d"))
    # data = ip_info_dao.get_ip_data_one_month(cur_time, 30)
    # data = ip_info_dao.get_ip_nums(cur_time, 2)
    # ip_info_dao.add_ip("127.0.0.1", cur_time.strftime("%Y-%m-%d"))
    # print(data)
