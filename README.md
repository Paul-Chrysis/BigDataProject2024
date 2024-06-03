# BigDataProject2024

## Project Overview

This project is developed for the Big Data Management Systems course at CEID for the 2024 second semester.

## Technologies Used

- Jupyter Notebooks
- Python (v3.9.6)
- Apache Kafka
- Apache Spark
- MongoDB
- UXSim [(GitHub)](https://github.com/toruseo/UXsim)
- Docker

## Python Modules

- UXSIM
- ipykernel
- schedule
- pandas
- datetime
- pyspark

## Docker Images

- wurstmeister/kafka:latest (Kafka)
- confluentinc/cp-zookeeper:latest (Zookeeper)
- bitnami/spark:latest (Spark)

## Tools used

- Visual Studio Code
- Offset Explorer 3.0

### Extensions

- Python (v2024.6.0)
- Python Debugger (v2024.6.0)
- Python Environment Manager (v1.2.4)
- Pylance (v2024.5.1)
- Jupyter (v2024.4.0)
- Docker (v1.29.1)
- Markdown All in One (v3.6.2)

## Project Requirements

1. **Data Generation:**
   - Develop a Python script that sends data to a Kafka broker at regular intervals based on the results of the uxsim simulator.
2. **Real-time Processing:**
   - Implement an Apache Spark application to perform real-time processing on the incoming data from the Kafka broker.
3. **Storage in NoSQL Database:**
   - Store both raw data and their processed form (by Spark) in a MongoDB implementation.

## Docker Setup

### Docker Network setup

```bash
 docker network create bdp-network
```

### Zookeeper setup

1. **Change Working Directory to Zookeeper Directory:**

   ```bash
   cd ./zookeeper
   ```

2. **Build Docker Image:**

   ```bash
   docker build -t bdp-zookeeper .
   ```

3. **Run Docker Container:**
   ```bash
   docker run -d --name bdp-zookeeper-container --network bdp-network bdp-zookeeper
   ```

### Kafka setup

1. **Change Working Directory to Kafka Directory:**

   ```bash
   cd ./kafka
   ```

2. **Build Docker Image:**

   ```bash
   docker build -t bdp-kafka .
   ```

3. **Run Docker Container:**

   ```bash
   docker run -d --name bdp-kafka-container --network bdp-network -p 9092:9092 -p 9093:9093 bdp-kafka
   ```

### Topic Creation setup

1. **Change Working Directory to topic_creator:**
   ```bash
   cd ./topic_creator
   ```
1. **Run kafka_topic_creator python script**
   ```bash
   python ./kafka_topic_creator.py
   ```

### Spark setup

1. **Change Working Directory to Spark Directory:**

   ```bash
   cd ./spark
   ```

2. **Build Docker Image:**

   ```bash
   docker build -t bdp-spark .
   ```

3. **Run Docker Container:**

   ```bash
   docker run -d --name bdp-spark-container --network bdp-network bdp-spark
   ```

### Message Creation setup

1. **Change Working Directory to message producer:**
   ```bash
   cd ./message_producer
   ```
2. **Run message_producer python script**
   ```bash
   python ./message_producer.py
   ```

### Additional Tips

> **Tip:** To interact with a service container, use the following command:
>
> ```bash
> docker exec -it bdp-{service}-container bash
> ```

> **Tip:** To remove a container:
>
> ```bash
> docker stop bdp-{service}-container
> docker rm bdp-{service}-container
> ```

## Docker-Compose setup

```bash
docker-compose up --build
```

> &#x26a0;&#xfe0f; **IMPORTANT**: The Kafka topics must be created after the Kafka container has been started, but before the Spark container setup begins.

1. **Change Working Directory to topic_creator:**
   ```bash
   cd ./topic_creator
   ```
1. **Run kafka_topic_creator python script**
   ```bash
   python ./kafka_topic_creator.py
   ```

> then use the message_producer script

### Message Creation setup

1. **Change Working Directory to message producer:**
   ```bash
   cd ./message_producer
   ```
2. **Run message_producer python script**
   ```bash
   python ./message_producer.py
   ```

## bibliography

- [spark - kafka connection](https://spark.apache.org/docs/latest/structured-streaming-kafka-integration.html)
