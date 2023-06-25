import os
import sqlite3

"""
系统配置
"""
# ip 更新时间间隔 (min)
IP_UPDATE_TIME = 5
# 查询GPU数据间隔
REFRESH_SEC = 5
# 20s调用接口 休眠线程
UPDATE_GAP = 20
# 配置需要监控的服务器
SERVERS_CONFIG = [
    # ('Server name', 'ip', 'user', 'password'),
]
"""
数据库配置
"""
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = str(BASE_DIR).replace('config', 'database')
print("db path: ", BASE_DIR)
db_path = os.path.join(BASE_DIR, "ip.db")
COON = sqlite3.connect(db_path, check_same_thread=False)
"""
管理员授权码
"""
AccessToken = ""