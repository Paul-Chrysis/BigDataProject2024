from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError
# from kafka import KafkaProducer, KafkaConsumer

bootstrap_servers = 'localhost:9092'

raw_data_topic_name = 'vehicle_positions'
spark_generated_data_topic_name = 'results'

num_partitions = 1
replication_factor = 1

admin_client = KafkaAdminClient(bootstrap_servers=bootstrap_servers)

raw_data_topic = NewTopic(name=raw_data_topic_name, num_partitions=num_partitions, replication_factor=replication_factor)
spark_generated_data_topic = NewTopic(name=spark_generated_data_topic_name, num_partitions=num_partitions, replication_factor=replication_factor)

try:
    new_topics = [raw_data_topic,spark_generated_data_topic]
    admin_client.create_topics(new_topics=new_topics)
    for topic_name in new_topics:
        print(f"Topic '{topic_name}' created successfully!")
except TopicAlreadyExistsError as e:
    print(f"Topic already exists.")
except Exception as e:
    print(f"An error occurred: {str(e)}")
finally:
    admin_client.close()