from concurrent.futures import ThreadPoolExecutor

from myapp_etl.consumers import consume_address, consume_name


def run_consumers():
    print("Starting Consumers")
    consumers = [consume_address, consume_name]
    with ThreadPoolExecutor() as executor:
        for consumer in consumers:
            executor.submit(consumer)

    print("Exiting Consumers")

if __name__ == '__main__':
    run_consumers()
