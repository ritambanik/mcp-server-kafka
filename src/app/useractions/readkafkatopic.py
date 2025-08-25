from kafkaconfig import conf
from mcp.types import TextContent

def read_kafka_topic(topic_name: str, timeout: int, limit: int = 10) -> list:
    """Read messages from a Kafka topic"""
    from confluent_kafka import Consumer, KafkaException, KafkaError
    import uuid
    
    consumer_conf = conf.copy()
    consumer_conf.update({
        'group.id': f"mcp-consumer-group-{str(uuid.uuid4())}",
        'auto.offset.reset': 'earliest'
    })
    
    consumer = Consumer(consumer_conf)
    consumer.subscribe([topic_name])
    
    messages = []
    
    try:
        for _ in range(limit):
            msg = consumer.poll(timeout=timeout)
            if msg is None:
                break
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition (not an error)
                    continue
                else:
                    raise KafkaException(msg.error())
            messages.append(TextContent(type="text", text=msg.value().decode('utf-8')))
    finally:
        consumer.close()
    
    return messages