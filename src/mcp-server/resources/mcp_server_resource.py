from __main__ import mcp

from mcp.types import TextContent
from typing import List
import json

@mcp.resource(
    uri="config://server-info",
    name="Server Information",
    description="Information about this MCP server",
    mime_type="application/json"
)
async def server_info_resource() -> List[TextContent]:
    """Provide server information"""
    server_info = {
        "name": "MCP Kafka Server",
        "version": "1.0.0",
        "description": "Example MCP server with Streamable HTTP transport using decorators",
        "capabilities": ["tools", "resources", "prompts"],
        "transport": "streamable-http",
        "tools": [
            "list_kafka_topics - List Kafka topics",
            "describe_kafka_topic - Describe a Kafka topic"
        ],
        "resources": [
            "config://server-info - Server configuration"
        ],
        "prompts": [
            "summarize - Create text summaries",
            "analyze - Analyze content"
        ]
    }
    
    return [TextContent(
        type="text",
        text=json.dumps(server_info, indent=2)
    )]