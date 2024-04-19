<div align="center">
<h1>GPU-Monitor</h1>
<p><em>Real-time monitoring of model training status, GPU resource utilization, model training logs, IP access records, etc.</em></p>
<p>Welcome to star, fork, and submit pull requests.</p>
</div>

## Main Features

- [x] Lightweight and Concise: Flask + SQLite3 + Vue3 + ElementUI-Plus
- [x] Quick Integration: Integration with new servers is as easy as a single line of configuration
- [x] Leisurely Alchemy: Real-time monitoring of model training progress
- [x] Logging System: Track changes in model loss and review training logs
- [x] Announcement Module: Timely delivery of important information
- [x] IP Statistics: Collect and display IP access information to enhance security awareness
- [x] Quick Card Grabbing: Real-time preview of GPU resource utilization
- [x] Low Resource Consumption: Multi-threaded controllable scheduling with minimal CPU usage
- [x] One-Click Deployment: Docker one-click deployment
- [x] Extensibility: Suitable for beginners to practice

## Preview

### Home Page

<table style="width: 100%">
<tr style="width: 100%;">
<td colspan="2" style="width: 100%;">
<img src="./img/main.png" alt="首页">
</td>
</tr>
</table>

### Announcement Module

<table style="width: 100%">
<tr style="width: 100%;">
<td colspan="2" style="width: 100%;">
<img src="./img/img_5.png" alt="首页">
</td>
</tr>
</table>

### GPU Server Details
<table style="width: 100%">
<tr style="width: 100%;">
<td colspan="2" style="width: 100%;">
<img src="./img/img_2.png" alt="首页">
</td>
</tr>
</table>


### Logging System

<table style="width: 100%">
<tr style="width: 100%;">
<td colspan="2" style="width: 100%;">
<img src="./img/log_1.png" alt="日志管理-弹窗">
</td>
</tr>
</table>

### Logging System

<table style="width: 100%">
<tr style="width: 100%;">
<td colspan="2" style="width: 100%;">
<img src="./img/img_3.png" alt="日志管理-弹窗">
</td>
</tr>
</table>

### Log Management
<table style="width: 100%">
<tr style="width: 100%;">
<td colspan="2" style="width: 100%;">
<img src="./img/img_4.png" alt="日志管理-弹窗">
</td>
</tr>
</table>

### View Logs

<table style="width: 100%">
<tr style="width: 100%;">
<td colspan="2" style="width: 100%;">
<img src="./img/log_3.png" alt="查看日志">
</td>
</tr>
</table>

### System Monitoring

<table style="width: 100%">
<tr style="width: 100%;">
<td colspan="2" style="width: 100%;">
<img src="./img/img.png" alt="系统监测">
</td>
</tr>
</table>

### Performance Oversight

<table style="width: 100%">
<tr style="width: 100%;">
<td colspan="2" style="width: 100%;">
<img src="./img/img_1.png" alt="系统监测">
</td>
</tr>
</table>


### Update Log or Change Log

<table style="width: 100%">
<tr style="width: 100%;">
<td colspan="2" style="width: 100%;">
<img src="./img/update.png" alt="更新日志">
</td>
</tr>
</table>


## Deployment Methods

### Docker Deployment Example

#### 1. Build the Image

```sh
docker-compose build
```

#### 2. Run the Service

```sh
docker-compose up -d
```

#### 3. Rebuild

```sh
docker stop gpumonitor_web & docker rm -f gpumonitor_web & docker rmi -f  219.216.65.59:5000/gpumonitor_web:latest & \
docker stop gpumonitor_server & docker rm -f gpumonitor_server & docker rmi -f  219.216.65.59:5000/gpumonitor_server:latest & \
```

# Appreciation
>If it can help you
<table style="width: 100%">
<tr style="width: 100%">
<td style="width: 30%;text-align: center;">
支付宝<br/>
<img src="./img/zfb.png" alt="支付宝">
</td>
<td style="width: 30%;text-align: center">
微信<br/>
<img src="./img/wx.png" alt="微信">
</td>
</tr>
</table>    


## Disclaimer

This project is open-sourced solely for educational purposes and shall not be used for any illegal activities. Otherwise, the consequences are your own responsibility and are not associated with me. Please retain the project's address when using it, thank you.
