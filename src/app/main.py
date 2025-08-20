#!/usr/bin/env python3
"""
MCP Server with Streamable HTTP Transport - Decorator-based Implementation

This example demonstrates how to create an MCP server using decorators (@tool, @resource, @prompt)
with the Streamable HTTP transport protocol. This approach provides a cleaner, more intuitive
way to define server capabilities.
"""


import json
import logging

from typing import Any, Dict, List

import uvicorn

from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mcp = FastMCP(name="mcp-server-kafka", json_response=False, stateless_http=False) 
  
     
@mcp.tool(
    name="list_kafka_topics",
    description="List all Kafka topics availble in the cluster. List controlled by RBAC rules",
)
async def list_kafka_topics_tool() -> List[TextContent]:
    """Show a list of Kafka topics"""
    return [
        TextContent(type="text", text="topics1"),
        TextContent(type="text", text="topics2"),
        TextContent(type="text", text="topics3"),
    ]

@mcp.tool(
    name="describe_kafka_topic",
    description="Describe a specific Kafka topic with details like partitions, replication factor, and configurations",
)
async def calculate_tool(topic_name: str) -> Dict[str, Any]:
    """Describe a Kafka topic with its details"""

    return {
        "topic": topic_name,
        "partitions": 3,
        "replication_factor": 2,
        "configs": {
            "cleanup.policy": "delete",
            "compression.type": "producer"
        }
    }
    
       
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
    
     
@mcp.prompt(
    name="summarize",
    description="Create a summary of provided text"
   )
async def summarize_prompt(text: str, length: str = "medium", style: str = "paragraph") -> str:
    """Generate a text summarization prompt"""
    
    length_instructions = {
        "short": "Keep the summary to 1-2 sentences maximum",
        "medium": "Provide a concise summary in 2-4 sentences",
        "long": "Create a detailed summary in 1-2 paragraphs"
    }
    
    style_instructions = {
        "bullet-points": "Format the summary as clear bullet points",
        "paragraph": "Write the summary as flowing paragraphs",
        "executive": "Structure as an executive summary with key takeaways"
    }
    
    length_guide = length_instructions.get(length, length_instructions["medium"])
    style_guide = style_instructions.get(style, style_instructions["paragraph"])
    
    prompt_text = f"""Please create a {length} summary of the following text using {style} format:

TEXT TO SUMMARIZE:
{text}

SUMMARY REQUIREMENTS:
- {length_guide}
- {style_guide}
- Focus on the most important information
- Maintain the original meaning and context
- Use clear, accessible language

Please provide your summary now:"""

    return prompt_text
    
@mcp.prompt(
    name="analyze",
    description="Analyze data or text content"
    )
async def analyze_prompt(content: str, focus: str = "general analysis", depth: str = "detailed") -> str:
    """Generate a content analysis prompt"""
    
    depth_instructions = {
        "surface": "Provide a high-level overview with main observations",
        "detailed": "Conduct a thorough analysis with specific examples and insights",
        "comprehensive": "Perform an in-depth analysis covering multiple dimensions and implications"
    }
    
    focus_examples = {
        "trends": "Look for patterns, changes over time, and emerging trends",
        "patterns": "Identify recurring themes, structures, and relationships",
        "sentiment": "Analyze emotional tone, attitudes, and opinions expressed",
        "structure": "Examine organization, flow, and logical arrangement",
        "general analysis": "Provide a well-rounded analysis covering key aspects"
    }
    
    depth_guide = depth_instructions.get(depth, depth_instructions["detailed"])
    focus_guide = focus_examples.get(focus, focus_examples["general analysis"])
    
    prompt_text = f"""Please analyze the following content with a focus on {focus}:

CONTENT TO ANALYZE:
{content}

ANALYSIS PARAMETERS:
- Focus Area: {focus}
- Analysis Depth: {depth}
- Specific Instructions: {focus_guide}
- Detail Level: {depth_guide}

ANALYSIS FRAMEWORK:
1. Key Observations: What stands out most prominently?
2. Detailed Findings: Specific insights related to your focus area
3. Patterns & Relationships: Connections and recurring elements
4. Implications: What do these findings suggest or mean?
5. Recommendations: Actionable insights or next steps (if applicable)

Please provide your analysis following this framework:"""

    return prompt_text

    
if __name__ == "__main__":
    """Main function to run the MCP server"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="MCP Server with Streamable HTTP Transport (Decorator-based)"
    )
    parser.add_argument("--host", default="localhost", help="Host to bind to (default: localhost)")
    parser.add_argument("--port", type=int, default=3000, help="Port to bind to (default: 3000)")
    parser.add_argument("--name", default="decorator-mcp-server", help="Server name")
    parser.add_argument("--log-level", default="INFO", 
                       choices=["DEBUG", "INFO", "WARNING", "ERROR"],
                       help="Logging level (default: INFO)")
    
    args = parser.parse_args()
    
    # Configure logging level
    logging.getLogger().setLevel(getattr(logging, args.log_level.upper()))
      # Start the server with Streamable HTTP transport
    uvicorn.run(mcp.streamable_http_app, host=args.host, port=args.port)