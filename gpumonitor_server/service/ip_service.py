import collections
import datetime

from dao.ip_dao import IpInfoDao


class IpService:
    def __init__(self, coon):
        self.ip_info_dao = IpInfoDao(coon)

    def add_ip(self, ip):
        self.ip_info_dao.add_ip(ip, datetime.datetime.now().strftime("%Y-%m-%d"))

    # 获取一个月内ip数据
    def gen_ip_data_one_month(self):
        # 获取一个月内的ip数据
        cur_time = datetime.datetime.now()
        ip_data_one_month = self.ip_info_dao.get_ip_data_one_month(cur_time, 30)
        # 格式化为
        """
         his_ip_data: {
                datetime: ['1122a', '1a',],
                details: [[次数,时间,大小,ip],] 
                }
        """
        date_dict = collections.defaultdict(list)
        for ip_data in ip_data_one_month:
            #   [时间,次数,大小,ip]
            date_dict[ip_data[1][5:]].append([str(ip_data[1])[5:], ip_data[2], ip_data[2], ip_data[0]])
        # 构造数据结构
        temp_datetime = list(date_dict.keys())
        temp_datetime.sort()
        temp_details = list()
        for date in temp_datetime:
            for cur_details in date_dict[date]:
                cur_details[0] = temp_datetime.index(cur_details[0])
                temp_details.append(cur_details)
        return {"datetime": temp_datetime, "details": temp_details}

    #     数据统计
    # 今日活跃用户

    def get_ip_nums_today(self):
        # 获取当天范围内的ip数量
        cur_time = datetime.datetime.now()
        days_ago = cur_time - datetime.timedelta(days=1)
        today_num = self.ip_info_dao.get_ip_nums(cur_time, 1)
        yesterday_num = self.ip_info_dao.get_ip_nums(days_ago, 1)
        # 相比昨日 上升/下降 百分比
        if yesterday_num == 0:
            percent = 0
        else:
            percent = (today_num - yesterday_num) / yesterday_num

        if percent > 0:
            compare_yesterday = 1
        else:
            compare_yesterday = 0
        return {"today_online_user_nums": today_num, "compare_yesterday": compare_yesterday,
                "compare_yesterday_value": str(round(percent * 100, 2)) + "%"}

    # 本月活跃用户
    def get_ip_nums_this_month(self):
        # 获取当天范围内的ip数量
        cur_time = datetime.datetime.now()
        month_ago = cur_time - datetime.timedelta(days=30)
        month_num = self.ip_info_dao.get_ip_nums(cur_time, 30)
        two_month_num = self.ip_info_dao.get_ip_nums(month_ago, 30)
        # 相比昨日 上升/下降 百分比
        if two_month_num == 0:
            percent = 0
        else:
            percent = (month_num - two_month_num) / two_month_num
        if percent > 0:
            compare_yesterday = 1
        else:
            compare_yesterday = 0
        return {"month_online_user_nums": month_num, "compare_last_month": compare_yesterday,
                "compare_last_month_value": str(round(percent * 100, 2)) + "%"}

    # 历史访问用户
    def get_ip_nums_history(self):
        history_online_user_nums = self.ip_info_dao.get_ip_nums_all()
        return {"history_online_user_nums": history_online_user_nums}


if __name__ == '__main__':
    from gpumonitor_server.config.setting import COON

    ip_service = IpService(COON)
    # data = ip_service.get_ip_nums_today()
    data = ip_service.get_ip_nums_this_month()
    print(data)
