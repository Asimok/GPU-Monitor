FROM python:3.9.5-slim-buster
LABEL author="Asimok"
LABEL email="maqi_neu@163.com"
LABEL version="1"

RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
RUN echo 'Asia/Shanghai' >/etc/timezone

RUN mkdir /usr/src/gpumonitor_server -p
COPY . /usr/src/gpumonitor_server
WORKDIR /usr/src/gpumonitor_server
RUN pip install -r requirements.txt -i  https://pypi.tuna.tsinghua.edu.cn/simple
RUN ls
WORKDIR /usr/src/gpumonitor_server
RUN ls
EXPOSE 7030
CMD python -u main.py