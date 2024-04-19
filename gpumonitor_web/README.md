## 项目结构

```shell
.
├── Dockerfile
├── README-zh.md
├── build.sh
├── dist
├── nginx # nginx配置
├── public
├── quick_deploy.sh
├── src # 核心代码
└── vue.config.js

```

## 部署方式参考

项目提供Docker部署方式，也可以直接在本地运行。

### 本地打包推送

```sh
docker build --platform linux/amd64 . -t 219.216.65.59:5000/gpumonitor_web:latest
docker push 219.216.65.59:5000/gpumonitor_web:latest
```

### 部署

```shell
docker pull 219.216.65.59:5000/gpumonitor_web:latest
docker run -d -p 31800:80 --restart always --name gpumonitor_web  219.216.65.59:5000/gpumonitor_web:latest
```

### 更新

```shell
docker stop gpumonitor_web & docker rm -f gpumonitor_web & docker rmi -f  219.216.65.59:5000/gpumonitor_web:latest & \
docker pull 219.216.65.59:5000/gpumonitor_web:latest & \
docker run -d -p 31800:80 --restart always --name gpumonitor_web  219.216.65.59:5000/gpumonitor_web:latest &
```
