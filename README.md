# Sample code for backtesting server using FastAPI & MySQL 
    runs on AWS EC2 t3.micro instance -> vCPU: 2, vRAM: 1GB 

##  How to setup?

### 1. Install Docker (For x86 CPU architecture, Ubuntu20.04) - Do following commands
    sudo apt-get update

    sudo apt-get install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

    sudo mkdir -p /etc/apt/keyrings

    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
      $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

    sudo apt-get update

    sudo apt-get install docker-ce docker-ce-cli containerd.io

    sudo usermod -aG docker ubuntu
    sudo -su ubuntu

### 2. Run MySQL container
    docker run --name mysql-container -e MYSQL_ROOT_PASSWORD=password -e TZ=Asia/Seoul -d -p 3306:3306 --ipc=host --net="host" mysql:latest

### 3. Build & Run this server
    cd /home/ubuntu/backtesting_server_sample
    docker build --tag backtest_server:1.0 .
    docker run -d --name backtest_server -p 8000:8000 --ipc=host --net="host" -v /home/ubuntu/backtesting_server_sample:/backtesting_server_sample backtest_server:1.0

### 4. (on your local computer) You will need to insert sample data to remote server - takes about 2 hours for t3.micro instance EBS gp3 volume type
    python insert_sample_data_req.py

### 5. (on your local computer) Sample request code - for backtesting all tickers, do tickers_list = None, takes about 2 hours for 2 thread AWS t3.micro / 5 min for 16 thread intel CPU
    from pprint import pprint
    import requests
    res = requests.post(
        "http://3.36.101.24:8000/backtest", 
        json={"tickers_list": ['BTCUSDT', 'AAVEUSDT', 'ADAUSDT', 'AGIXUSDT', 'ACHUSDT']},
    )
    pprint(res.json())
    >>> {
            'result': [
                {'buy_and_hold_return_percent': 701.7185581371809,
                 'end': '2023-07-10 15:00:00',
                 'maximum_draw_down_percent': -82.16715014247042,
                 'overall_return_percent': -20.97965199340094,
                 'sharpe_ratio': 0.0,
                 'start': '2019-01-01 00:00:00',
                 'ticker': 'BTCUSDT'},
                {'buy_and_hold_return_percent': 40.15973868185712,
                 'end': '2023-07-10 15:30:00',
                 'maximum_draw_down_percent': -97.6866719402462,
                 'overall_return_percent': -92.14166450532001,
                 'sharpe_ratio': 0.0,
                 'start': '2020-10-15 12:00:00',
                 'ticker': 'AAVEUSDT'}, ...
            ]
        }

### (optional) 6. API Docs
    http://3.36.101.24:8000/docs