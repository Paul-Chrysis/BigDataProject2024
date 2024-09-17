import logging
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, avg, count , to_timestamp
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType, TimestampType
import time

kafka_server = "bdp-kafka-container:9093"
input_topic = "vehicle_positions"
output_topic = "results"
spark = SparkSession.builder\
    .appName("BigDataProcessing")\
    .config("spark.master", "local[*]") \
    .config('spark.kafka.bootstrap.servers', kafka_server)\
    .config("spark.mongodb.read.connection.uri", "mongodb://bdp-mongo-container:27017/bdp-database") \
    .config("spark.mongodb.write.connection.uri", "mongodb://bdp-mongo-container:27017/bdp-database") \
    .getOrCreate()

logging.basicConfig(level=logging.ERROR)
spark.sparkContext.setLogLevel("ERROR")

sc = spark.sparkContext


def saveRawData(message, batch_id):
    message.write \
    .format("mongodb")\
    .mode("append") \
    .option("database", "bdp-database") \
    .option("collection", "raw_data") \
    .save()
    message.show()

def saveProcessedData(message, batch_id):
    message.write \
    .format("mongodb")\
    .mode("append") \
    .option("database", "bdp-database") \
    .option("collection", "processed_data") \
    .save()
    message.show()

def check_topic_existence():
    try:   
        df = spark.read \
            .format("kafka") \
            .option("kafka.bootstrap.servers", kafka_server) \
            .option("failOnDataLoss", "false") \
            .option("subscribe", input_topic) \
            .load()
        return True
    except Exception as e:
        print(e)
        return False

while not check_topic_existence():
    print("Waiting for Kafka topic to be created...")
    time.sleep(10)

raw_schema = StructType([
    StructField("name", IntegerType(), True),
    StructField("dn", IntegerType(), True),
    StructField("origin", StringType(), True),
    StructField("destination", StringType(), True),
    StructField("time", StringType(), True),
    StructField("link", StringType(), True),
    StructField("position", DoubleType(), True),
    StructField("spacing", DoubleType(), True),
    StructField("speed", DoubleType(), True)
])

processed_schema = StructType([
    StructField("time", StringType(), True),
    StructField("link", StringType(), True),
    StructField("vcount", DoubleType(), True),
    StructField("vspeed", DoubleType(), True),
])

df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_server) \
    .option("subscribe", input_topic) \
    .load()

json_df = df.selectExpr("CAST(value AS STRING) as value") \
    .select(from_json(col("value"), raw_schema).alias("data")) \
    .select("data.*")

json_df = json_df.withColumn("time", to_timestamp(col("time"), "dd/MM/yyyy HH:mm:ss"))

result_df = json_df.withWatermark("time", "10 seconds") \
    .groupBy("link", "time") \
    .agg(
        count("name").alias("vcount"),
        avg("speed").alias("vspeed")
    )

# write to raw
query_raw = json_df.writeStream.foreachBatch(saveRawData).start()
# write to processed
query_processed = result_df.writeStream.foreachBatch(saveProcessedData).start()
# convert df to write to kafka
output_df = result_df.selectExpr("CAST(link AS STRING) AS key", "to_json(struct(*)) AS value")
# write to kafka
query_kafka = output_df \
.writeStream \
.format("kafka") \
.option("kafka.bootstrap.servers", kafka_server) \
.option("topic", output_topic) \
.option("checkpointLocation", "checkpoint/") \
.start()

query_raw.awaitTermination()
query_processed.awaitTermination()
query_kafka.awaitTermination()