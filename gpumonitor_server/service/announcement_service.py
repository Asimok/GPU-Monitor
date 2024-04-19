from config.setting import COON
from dao.announcement_dao import AnnouncementDao


class AnnouncementService:
    def __init__(self, coon):
        self.announcement_dao = AnnouncementDao(coon)

    # 新增公告
    def add_announcement(self, announcement, expire_date, available=1, times=1):
        self.announcement_dao.add_announcement(announcement=announcement, expire_date=expire_date, available=available,
                                               times=times)

    # 删除公告
    def del_announcement_by_id(self, id):
        self.announcement_dao.del_announcement_by_id(id)

    # 获取当前ip可阅读公告
    def get_announcement_by_ip(self, ip):
        res = []
        _data = self.announcement_dao.get_all_announcement_by_ip(ip=ip)
        for tmp in _data:
            res.append(list(tmp))
        return res

    # 标记当前用户阅读公告
    def add_push_info(self, ip, announcement_id):
        self.announcement_dao.add_push_info(ip=ip, announcement_id=announcement_id)

    # 得到所有历史公告的数据
    def get_all_history_announcement(self):
        res = []
        _data = self.announcement_dao.get_all_history_announcement()
        for tmp in _data:
            res.append(list(tmp))
        return res[::-1]


if __name__ == '__main__':
    announcementService = AnnouncementService(COON)
    data = announcementService.get_announcement_by_ip(ip="12.121.121.12")
    pass
