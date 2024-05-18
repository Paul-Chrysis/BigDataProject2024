from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError
# from kafka import KafkaProducer, KafkaConsumer

bootstrap_servers = 'localhost:9092'

topic_name = 'vehicle_positions'
num_partitions = 3
replication_factor = 1

admin_client = KafkaAdminClient(bootstrap_servers=bootstrap_servers)

new_topic = NewTopic(name=topic_name, num_partitions=num_partitions, replication_factor=replication_factor)

try:
    admin_client.create_topics(new_topics=[new_topic])
    print(f"Topic '{topic_name}' created successfully!")
except TopicAlreadyExistsError as e:
    print(f"Topic '{topic_name}' already exists.")
except Exception as e:
    print(f"An error occurred: {str(e)}")
finally:
    admin_client.close()