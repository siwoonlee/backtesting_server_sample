# Sample code for backtesting server using FastAPI & MySQL 
    runs on AWS EC2 t3.micro instance -> vCPU: 2, vRAM: 1GB 

### You will need to insert sample data to remote server
    python insert_sample_data_req.py

### Sample request code
    import requests
    res = requests.get("http://3.35.197.182:8000/backtest")
    print(res.json())

### How To Install Docker & Docker-Compose (For x86 CPU architecture, Ubuntu20.04)
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
    sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin

    sudo usermod -aG docker ubuntu
    sudo -su ubuntu


### Run MySQL container
    docker run --name mysql-container -e MYSQL_ROOT_PASSWORD=password -e TZ=Asia/Seoul -d -p 3306:3306 --ipc=host --net="host" mysql:latest

### Build & Run this server
    docker build --tag backtest_server:1.0 .
    docker run -d --name backtest_server -p 8000:8000 --ipc=host --net="host" -v /home/ubuntu/backtesting_server_sample:/backtesting_server_sample backtest_server:1.0

