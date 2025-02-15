FROM python:3.12
ENV PYTHONUNBUFFERED 1
# RUN apt-get update
# RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash -
# RUN apt-get install -y nodejs
RUN apt update
RUN apt install -y libgl1-mesa-glx
RUN apt install libffi-dev
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
# RUN pip install -i https://pypi.douban.com/simple -U pip
# RUN pip install -i https://pypi.douban.com/simple -r requirements.txt
RUN pip install -U pip
RUN pip install -r requirements.txt

RUN rm -f /etc/localtime
RUN  ln -s /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' > /etc/timezone

COPY . /code/
