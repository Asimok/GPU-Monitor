## 项目结构
```shell
.
├── Dockerfile
├── README.md
├── config # 系统配置
├── core # 核心代码
├── dao # 数据库操作
├── database # 数据库
├── main.py # rest API
├── requirements.txt 
├── service # 业务逻辑
└── utils # 工具类
```


## 部署方式参考

项目提供Docker部署方式，也可以直接在本地运行。

### 本地打包推送

```shell
docker build --platform linux/amd64 . -t 219.216.65.59:5000/gpumonitor_server:latest
docker push 219.216.65.59:5000/gpumonitor_server:latest
```

### 部署

```shell
docker pull 219.216.65.59:5000/gpumonitor_server:latest
docker run -d -p 7030:7030 --restart always --name gpumonitor_server  219.216.65.59:5000/gpumonitor_server:latest
```

### 更新

```shell
docker stop gpumonitor_server & docker rm -f gpumonitor_server & docker rmi -f  219.216.65.59:5000/gpumonitor_server:latest & \
docker pull 219.216.65.59:5000/gpumonitor_server:latest & \
docker run -d -p 7030:7030 --restart always --name gpumonitor_server -v /data0/maqi/maqi_server/gpumonitor_server/database:/usr/src/gpumonitor_server/database 219.216.65.59:5000/gpumonitor_server:latest &
```
