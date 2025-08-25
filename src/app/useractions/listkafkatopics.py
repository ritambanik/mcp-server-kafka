from kafkaconfig import admin_client
from typing import List

def list_kafka_topics()->List[str]:
    """List all Kafka topics available in the cluster."""
    cluster_metadata = admin_client.list_topics(timeout=10)
    topic_names = cluster_metadata.topics.keys()
    return list(topic_names)