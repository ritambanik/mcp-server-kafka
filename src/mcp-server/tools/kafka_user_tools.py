from __main__ import mcp

from mcp.types import TextContent
from typing import Any, Dict, List

@mcp.tool(
    name="list_kafka_topics",
    description="List all Kafka topics availble in the cluster. List controlled by RBAC rules",
)
async def list_kafka_topics_tool() -> List[TextContent]:
    """Show a list of Kafka topics""" 
    from kafka.useractions.listkafkatopics import list_kafka_topics
    
    topic_names = list_kafka_topics() 
    return [TextContent(type="text", text=f"{topic_name}\n") for topic_name in topic_names]
    

@mcp.tool(
    name="describe_kafka_topic",
    description="Describe a specific Kafka topic with details like partitions, replication factor, and configurations",
)
async def describe_kafka_topic(topic_name: str) -> Dict[str, Any]:
    """Describe a Kafka topic with its details"""
    
    from kafka.useractions.describekafkatopic import describe_kafka_topic
    
    topic_info = describe_kafka_topic(topic_name)
    return topic_info
    
@mcp.tool(
       name="read_kafka_topic",
       description="Read messages from a specific Kafka topic",
         )
async def read_kafka_topic(topic_name: str, limit: int = 10, timeout : int = 30) -> List[TextContent]:
    """Read messages from a Kafka topic"""
    
    from kafka.useractions.readkafkatopic import read_kafka_topic
    messages = read_kafka_topic(topic_name, timeout=timeout, limit=limit)
    return messages