from kafka import KafkaConsumer, TopicPartition
from kafka.errors import KafkaError

bootstrap_servers = 'localhost:9092'
topic_name = 'vehicle_positions'

def consume():
    consumer = KafkaConsumer(bootstrap_servers=bootstrap_servers,
                             auto_offset_reset='earliest')
    
    partitions = consumer.partitions_for_topic(topic_name)
    if partitions is None:
        print(f"Topic '{topic_name}' not found.")
        return

    try:
        for partition in partitions:
            topic_partition = TopicPartition(topic_name, partition)
            consumer.assign([topic_partition])
            consumer.seek_to_beginning(topic_partition)
            for message in consumer:
                print(f"Consumed message from partition {partition}: {message.value.decode('utf-8')}")
    except KafkaError as e:
        print(f"Error consuming messages: {e}")
    except KeyboardInterrupt:
        print("Stopping consumer...")    
    finally:
        consumer.close()
        print("Consumer closed.")   

if __name__ == "__main__":
    consume()
