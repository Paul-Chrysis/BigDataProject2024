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
- python:3.9-slim
- mongo:latest

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
- Pymongo (v4.8.0)

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

### Kafka Topic Creator setup

1. **Change Working Directory to Topic Creator Directory:**

   ```bash
   cd ./topic_creator
   ```

2. **Build Docker Image:**

   ```bash
   docker build -t bdp-kafka-topic .
   ```

3. **Run Docker Container:**

   ```bash
   docker run -d --name bdp-kafka-topic-container --network bdp-network -p 9092:9092 -p 9093:9093 bdp-kafka-topic
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

### Mongo setup

1. **Change Working Directory to Mongo Directory:**

   ```bash
   cd ./mongo
   ```

2. **Build Docker Image:**

   ```bash
   docker build -t bdp-mongo .
   ```

3. **Run Docker Container:**

   ```bash
   docker run -d --name bdp-mongo-container --network bdp-network bdp-mongo
   ```

### Mongo-Config setup

1. **Change Working Directory to mongo config Directory:**

   ```bash
   cd ./mongo_config
   ```

2. **Build Docker Image:**

   ```bash
   docker build -t bdp-mongo-config .
   ```

3. **Run Docker Container:**

   ```bash
   docker run -d --name bdp-mongo-config-container --network bdp-network bdp-mongo-config
   ```

### Message Producer setup

1. **Change Working Directory to Message producer Directory:**

   ```bash
   cd ./message_producer
   ```

2. **Build Docker Image:**

   ```bash
   docker build -t bdp-message-producer .
   ```

3. **Run Docker Container:**

   ```bash
   docker run -d --name bdp-message-producer-container --network bdp-network bdp-message-producer
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

## bibliography

- [spark - kafka connection](https://spark.apache.org/docs/latest/structured-streaming-kafka-integration.html)
- [write to mongo](https://www.mongodb.com/docs/spark-connector/upcoming/streaming-mode/streaming-write/)
