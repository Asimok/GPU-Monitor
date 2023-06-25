import datetime
import random

from cffi.cparser import lock

from config.setting import COON, IP_UPDATE_TIME


class AnnouncementDao:
    def __init__(self, coon):
        self.conn = coon
        self.c = self.conn.cursor()
        # 判断数据表 announcement_info 是否存在 不存在则创建
        self.c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='announcement_info'")
        result = self.c.fetchone()
        if result is not None:
            print("数据表 announcement_info 已存在")
        else:
            print("数据表 announcement_info 不存在,即将创建")
            self.c.execute(
                '''CREATE TABLE IF NOT EXISTS announcement_info (id INTEGER PRIMARY KEY, date DATE, expire_date DATE, times INTEGER, available INTEGER,announcement TEXT)''')
        # 判断数据表 push_info 是否存在 不存在则创建
        self.c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='push_info'")
        result = self.c.fetchone()
        if result is not None:
            print("数据表 push_info 已存在")
        else:
            print("数据表 push_info 不存在,即将创建")
            self.c.execute(
                '''CREATE TABLE IF NOT EXISTS push_info (ip TEXT, announcement_id INTEGER,times INTEGER)''')

    # 新增公告
    def add_announcement(self, announcement, expire_date, available, times):
        try:
            lock.acquire(True)
            _cur_time = datetime.datetime.now()
            # 当前时间加上过期时间
            expire_date = _cur_time + datetime.timedelta(days=expire_date)
            self.c.execute(
                "INSERT INTO announcement_info (id,date,expire_date,times,available,announcement) VALUES (NULL,?,?,?,?,?)",
                (_cur_time, expire_date, times, available, announcement))
            self.conn.commit()
        finally:
            lock.release()

    # 根据id删除公告
    def del_announcement_by_id(self, id):
        try:
            lock.acquire(True)
            self.c.execute("DELETE FROM announcement_info WHERE id = ?", (id,))
            self.conn.commit()
        finally:
            lock.release()

    # 查询未过期的所有公告
    def get_all_announcement(self):
        _cur_time = datetime.datetime.now()
        self.c.execute(
            "SELECT id, date,expire_date,times,available,announcement FROM announcement_info WHERE expire_date > ?",
            (_cur_time,))
        result = self.c.fetchall()
        return result

    # 查询当前用户所有未阅读的公告
    def get_all_announcement_by_ip(self, ip):
        announcement_list = self.get_all_announcement()
        result = []
        for announcement in announcement_list:
            # 判断当前用户是否已经阅读过该公告
            if self.get_announcement_by_ip(ip, announcement[0]):
                result.append(announcement)
        return result

    # 判断当前用户是否可以阅读该公告
    def get_announcement_by_ip(self, ip, announcement_id):
        # 查询当前ip是否已经阅读过该公告 且 次数小于可阅读次数
        self.c.execute("SELECT * FROM push_info WHERE ip = ? and announcement_id = ?", (ip, announcement_id))
        result = self.c.fetchone()
        if result is not None:
            # 如果已经阅读过该公告 且 次数小于可阅读次数
            self.c.execute("SELECT times FROM announcement_info WHERE id = ?", (announcement_id,))
            _times = self.c.fetchone()
            if result[2] < _times[0]:
                return True
            else:
                return False
        else:
            return True

    # 标记当前用户已经阅读过该公告
    def add_push_info(self, ip, announcement_id):
        try:
            lock.acquire(True)
            # 判断当前用户是否已经阅读过该公告
            self.c.execute("SELECT * FROM push_info WHERE ip = ? and announcement_id = ?", (ip, announcement_id))
            result = self.c.fetchone()
            if not result is None:
                self.c.execute("UPDATE push_info SET times = times + 1 WHERE ip = ? and announcement_id = ?",
                               (ip, announcement_id))
                self.conn.commit()
            else:
                self.c.execute("INSERT INTO push_info (ip, announcement_id,times) VALUES (?,?,?)",
                               (ip, announcement_id, 1))
                self.conn.commit()
        finally:
            lock.release()

    # 查询所有公告--for 历史公告
    def get_all_history_announcement(self):
        _cur_time = datetime.datetime.now()
        self.c.execute(
            "SELECT id, date, expire_date, times, announcement FROM announcement_info" )
        result = self.c.fetchall()
        return result

if __name__ == '__main__':
    coon = COON
    announcement_dao = AnnouncementDao(coon)
    cur_time = datetime.datetime.now()
    # announcement_dao.add_announcement(announcement="第二条测试", expire_date=3, available=1, times=5)
    # data = announcement_dao.get_all_announcement()
    # data = announcement_dao.get_announcement_by_ip(ip="12.121.121.12", announcement_id=3)
    # announcement_dao.add_push_info(ip="12.121.121.12", announcement_id=3)
    # data = announcement_dao.get_all_announcement_by_ip(ip="12.121.121.12")
    pass
