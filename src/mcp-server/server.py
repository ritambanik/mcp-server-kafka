#!/usr/bin/env python3
"""
MCP Server with Streamable HTTP Transport - Decorator-based Implementation

This example demonstrates how to create an MCP server using decorators (@tool, @resource, @prompt)
with the Streamable HTTP transport protocol. This approach provides a cleaner, more intuitive
way to define server capabilities.
"""



import logging
import uvicorn
from mcp.server.fastmcp import FastMCP


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mcp = FastMCP(name="mcp-server-kafka", json_response=False, stateless_http=False)

from tools import kafka_user_tools
from resources import mcp_server_resource
from prompts import code_analysis_prompt, code_summarization_prompt

    
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