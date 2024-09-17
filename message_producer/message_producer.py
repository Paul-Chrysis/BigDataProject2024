import json
import time
import pandas as pd
from datetime import datetime, timedelta
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
import schedule
import time

bootstrap_servers = 'bdp-kafka-container:9093'
topic_name = 'vehicle_positions'
interval_seconds = 5
start_time = datetime.now()
simulation_interval_time = 0
file_path = './sources/sorted_vehicles.csv'
retries = 5 
continue_message_sending = True 
topic_created = False


while not topic_created:
    time.sleep(5)
    try:
        producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        topic_created = True
    except NoBrokersAvailable:
        print(f"Kafka broker is not available. Trying again in 5 seconds")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def read_data_from_csv(file_path,time_frame):
    df = pd.read_csv(file_path)
    selected_rows = df[df['t'] == time_frame]
    data = selected_rows.to_dict(orient='records')
    return data

def prepare_record(record, start_time):
    t = int(record["t"])
    send_time = start_time + timedelta(seconds=t)
    prepared_record = {
        "name": record["name"],
        "dn": record["dn"],
        "origin": record["orig"],
        "destination": record["dest"],
        "time": send_time.strftime("%d/%m/%Y %H:%M:%S"),
        "link": record["link"],
        "position": float(record["x"]),
        "spacing": float(record["s"]),
        "speed": float(record["v"])
    }
    return prepared_record

def send_to_kafka(producer, topic, record):
    producer.send(topic, record)
    print(f"Sent record to Kafka: {record}")

def job(producer, topic, file_path, start_time, interval_seconds):
    global retries, simulation_interval_time, continue_message_sending
    data = read_data_from_csv(file_path, simulation_interval_time)
    print("Doing Job")
    if len(data) > 0:
        for data_record in data:
          record = prepare_record(data_record, start_time)
          if record["link"] != "trip_end" and record["link"] != "waiting_at_origin_node":
              send_to_kafka(producer, topic, record)
        retries = 5
    elif retries == 0:
        print("All data has been sent. Stopping the scheduler.")
        continue_message_sending = False
        return schedule.CancelJob
    else:
        retries = retries - 1
        print(f"No data to send remaining retries: {retries}")
    simulation_interval_time += interval_seconds

schedule.every(1).seconds.do(job, producer, topic_name, file_path, start_time, interval_seconds)

try:
    while continue_message_sending:
        print("Schedule Work")
        schedule.run_pending() 
        time.sleep(1)  
except KeyboardInterrupt:
    print("Stopping producer...")
finally:
    producer.close()
    print("Producer closed.")
