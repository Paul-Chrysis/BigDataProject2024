from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, avg, count , to_timestamp
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType
import time

kafka_server = "bdp-kafka-container:9093"
input_topic = "vehicle_positions"
output_topic = "results"
spark = SparkSession.builder\
    .appName("BigDataProcessing")\
    .config('spark.kafka.bootstrap.servers', kafka_server)\
    .getOrCreate()

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

schema = StructType([
    StructField("name", IntegerType(), True),
    StructField("origin", StringType(), True),
    StructField("destination", StringType(), True),
    StructField("time", StringType(), True),
    StructField("link", StringType(), True),
    StructField("position", DoubleType(), True),
    StructField("spacing", DoubleType(), True),
    StructField("speed", DoubleType(), True)
])

df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_server) \
    .option("subscribe", input_topic) \
    .load()

json_df = df.selectExpr("CAST(value AS STRING) as value") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

json_df = json_df.withColumn("time", to_timestamp(col("time"), "dd/MM/yyyy HH:mm:ss"))

result_df = json_df.withWatermark("time", "10 seconds") \
    .groupBy("link", "time") \
    .agg(
        count("name").alias("vcount"),
        avg("speed").alias("vspeed")
    )

output_df = result_df.selectExpr("CAST(link AS STRING) AS key", "to_json(struct(*)) AS value")

query = output_df \
.writeStream \
.format("kafka") \
.option("kafka.bootstrap.servers", kafka_server) \
.option("topic", output_topic) \
.option("checkpointLocation", "checkpoint/") \
.start()

query.awaitTermination()