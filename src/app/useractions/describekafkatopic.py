from kafkaconfig import admin_client

def describe_kafka_topic(topic_name: str) -> dict:
    """Describe a Kafka topic with its details"""
    
    try:
        # Get cluster metadata which includes topic information
        metadata = admin_client.list_topics(topic=topic_name, timeout=10)
        
        if topic_name in metadata.topics:
            topic = metadata.topics[topic_name]
            
            # Build detailed response
            topic_info = {
                "topic_name": topic_name,
                "partition_count": len(topic.partitions),
                "partitions": {}
            }
            
            # Add partition details
            for partition_id, partition in topic.partitions.items():
                topic_info["partitions"][partition_id] = {
                    "leader": partition.leader,
                    "replicas": partition.replicas,
                    "isrs": partition.isrs
                }
            
            return topic_info
        else:
            return {"error": f"Topic '{topic_name}' does not exist."}
    
    except Exception as e:
        return {"error": str(e)}