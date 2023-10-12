import os
from concurrent.futures import ThreadPoolExecutor
from time import sleep

from kafka import KafkaClient
from kafka.errors import NoBrokersAvailable

from consumer.consumers import consume_clean, consume_raw

def wait_for_kakfa():
    attempts = 0
    while True:
        print("Waiting for Kafka")
        try:
            client = KafkaClient(bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS"))
            if client.bootstrap_connected():
                print("Connected to Kafka")
                client.close()
                return
        except NoBrokersAvailable:
            sleep(5)
            attempts += 1
        
        if attempts >= 20:
            raise NoBrokersAvailable
    

def run_consumers():
    print("Running Consumers")
    consumers = [consume_clean, consume_raw]
    with ThreadPoolExecutor() as executor:
        for consumer in consumers:
            executor.submit(consumer)

    print("Exiting Consumers")

if __name__ == '__main__':
    wait_for_kakfa()
    run_consumers()

