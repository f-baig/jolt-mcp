#!/usr/bin/env python3
import os
import sys
import json
import requests
import logging
from fastmcp import FastMCP
from dotenv import load_dotenv

# Set up logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

load_dotenv()

mcp = FastMCP("jolt-mcp")

# @mcp.tool(description="Print out a users api token.")
# def print_token(user_api_token: str) -> str:
#     """Print out a user's API token."""
#     try:
#         if not user_api_token:
#             return "Error: API token is required"
#         return f"Hello, {user_api_token}! This is your api token!"
#     except Exception as e:
#         logger.error(f"Error in print_token: {e}")
#         return f"Error processing token: {str(e)}"

# @mcp.tool(description="Print out a users name.")
# def print_name(name: str) -> str:
#     """Print out a user's name."""
#     try:
#         if not name:
#             return "Error: Name is required"
#         return f"Hello, {name}! Welcome to our sample HTTP server running on Nikhil!"
#     except Exception as e:
#         logger.error(f"Error in print_name: {e}")
#         return f"Error processing name: {str(e)}"

@mcp.tool(description="Print out a users email.")
def get_email(user_api_token: str) -> str:
    headers = {"Authorization": f"Bearer {user_api_token}"}
    return requests.get(f"https://jolt.nikhilrado.com/api/v1/email", headers=headers, timeout=10).json()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
            
    # Run with proper error handling
    mcp.run(
        transport="http",
        host=host,
        port=port
    )