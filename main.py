"""
  A MCP server for connecting to Kafka cluster and executing queries
"""

import os
from dotenv import load_dotenv

from fastapi import FastAPI
from datetime import datetime
import time

from mcp.server.fastmcp import FastMCP


load_dotenv()

mcp = FastMCP(name="mcp-server-kafka",stateless_http=True, host="0.0.0.0", port=8000)

app = FastAPI(title="mcp-server-kafka",lifespan=lambda app: mcp.session_manager.run())
app.mount("/health", mcp.streamable_http_app())
start_time = time.time()

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "mcp-server-kafka",
        "timestamp": datetime.now(datetime.timezone.utc).isoformat(),
        "uptime": time.time() - start_time
    }


@mcp.tool("list_kafka_topics")
def list_kafka_topics() -> list:
    # Placeholder function to list Kafka topics
    return ["topic1", "topic2", "topic3"]

@mcp.tool("describe_kafka_topic")
def describe_kafka_topic(topic_name: str) -> dict:
    # Placeholder function to describe a Kafka topic
    return {
        "topic": topic_name,
        "partitions": 3,
        "replication_factor": 2,
        "configs": {
            "cleanup.policy": "delete",
            "compression.type": "producer"
        }
    }


def main():
    """Run the MCP server"""
    print("🌤️ Starting Kafka MCP Server...")
    print("📍 Supported functionalities:")
    print("  - List Kafka topics (list_kafka_topics)")
    print("  - Describe a Kafka topic (describe_kafka_topic)")
    
    mcp.run(transport="streamable-http")
    
    print("🚀 Server is running and ready to accept requests.")


if __name__ == "__main__":
    main()
