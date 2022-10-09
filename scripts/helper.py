import json
import pandas as pd
from kafka import KafkaProducer
from kafka.errors import KafkaError


def produce_the_message():
    raw_data_ = pd.read_csv('../data/raw_data.csv')
    print(raw_data_.shape)

    raw_data = raw_data_.iloc[0:3, ]
    raw_data = raw_data.to_dict()

    print('publishing raw message . . .')
    # raw_data = ti.xcom_pull(key='raw_data_from_csv', task_ids='raw_data_read')

    # TODO" uncomment the next two lines to print data info
    #print(f'data: {raw_data}\ntype of the data: {type(raw_data)}')
    #print(f'using json.dumps: {json.dumps(raw_data, indent=4)}')
    print('raw message received . . .')

    RAW_DATA_TOPIC = 'g1-raw-text-data-topic-dev'
    print(f'publishing raw messages to the {RAW_DATA_TOPIC} topic . . .')
    aws_instance_bootstrap_servers = ['b-1.batch6w7.6qsgnf.c19.kafka.us-east-1.amazonaws.com:9092',
                                      'b-2.batch6w7.6qsgnf.c19.kafka.us-east-1.amazonaws.com:9092']

    producer = KafkaProducer(bootstrap_servers=aws_instance_bootstrap_servers)
    # producer = KafkaProducer(
    #    value_serializer=lambda v: json.dumps(v).encode("utf-8"))

    # print(f"article: {raw_data['article']}")
    # print(f"keys: {raw_data['article'].keys()}")
    # print(f"values: {raw_data['article'].values()}")
    for i in range(0, 3):
        print(f"{i}: {type(raw_data['article'][i])}")
        print(raw_data['article'][i])
        # producer.send(RAW_DATA_TOPIC, key=i, value=raw_data['article'][i])
        future = producer.send(RAW_DATA_TOPIC, b'test message . . . ')
        try:
            record_metadata = future.get(timeout=10)
        except KafkaError:
            # Decide what to do if produce request failed...
            log.exception()
            pass

        # Successful result returns assigned partition and offset
        print(record_metadata.topic)
        print(record_metadata.partition)
        print(record_metadata.offset)

    print('publishing raw messages completed. . .')


produce_the_message()
