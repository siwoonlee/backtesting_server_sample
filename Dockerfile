FROM python:3.10-slim-buster

RUN apt update && apt install -y \
    build-essential \
    gcc \
    libsasl2-modules  \
    libsasl2-dev \
    tmux

RUN ln -snf /usr/share/zoneinfo/Asia/Seoul /etc/localtime && echo Asia/Seoul > /etc/timezone

RUN mkdir /backtest_server_sample
VOLUME ["/backtest_server_sample"]

COPY . /backtest_server_sample
WORKDIR /backtest_server_sample
RUN pip install -r requirements.txt


CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port 8000 --reload"]