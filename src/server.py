#!/usr/bin/env python3
import os
import requests
from fastmcp import FastMCP

from dotenv import load_dotenv
load_dotenv()

mcp = FastMCP("jolt-mcp")

# @mcp.tool(description="Greet a user by name with a welcome message from the MCP server")
# def greet(name: str) -> str:
#     return f"Hello, {name}! Welcome to our sample MCP server running on Heroku!"

# @mcp.tool(description="Get information about the MCP server including name, version, environment, and Python version")
# def get_server_info() -> dict:
#     return {
#         "server_name": "Sample MCP Server",
#         "version": "1.0.0",
#         "environment": os.environ.get("ENVIRONMENT", "development"),
#         "python_version": os.sys.version.split()[0]
#     }

@mcp.tool
def jolt_user_id(
    userHandle: str,
    bearerToken: str,
):
    """
    Get information about the user's jolt ID.
    """
    base = os.getenv("FITNESS_API_BASE", "https://jolt.nikhilrado.com/api")
    headers = {"Authorization": f"Bearer {os.getenv(bearerToken,'')}"}
    return requests.get(f"{base}/v1/email", headers=headers, timeout=10).json()

# @mcp.tool
# def fitness_start_plan(
#     userHandle: str,
#     goal: str | None = None,
#     startDate: str | None = None,
# ):
#     """
#     Start a personalized fitness plan using OurSite run + meal data.
#     Use when the user says things like:
#     - "start a fitness plan", "make me a training plan", "new fitness program"
#     - "meal + run plan", "set up a running plan"
#     Inputs:
#       - userHandle: the user's handle/ID on OurSite
#       - goal (optional): e.g. "5K in 6 weeks", "lose 5 lb"
#       - startDate (optional): ISO date (YYYY-MM-DD)
#     Output: { planPreviewMd, nextAction, debug }
#     """
#     # Fetch from your website’s API (replace base + auth as needed)
#     base = os.getenv("FITNESS_API_BASE", "https://jolt.nikhilrado.com/api")
#     headers = {"Authorization": f"Bearer {os.getenv('FITNESS_API_KEY','')}"}

#     email  = requests.get(f"{base}/v1/email",  params={"user": "nr10+n1@williams.edu", "window": "90d"}, headers=headers, timeout=10).json()
#     # meals = requests.get(f"{base}/v1/email", params={"user": userHandle, "window": "90d"}, headers=headers, timeout=10).json()

#     # toy logic for a preview
#     # weekly_miles = sum(r.get("miles", 0) for r in runs[-7:])
#     # protein_avg  = round(sum(m.get("protein_g", 0) for m in meals[-7:]) / max(1, len(meals[-7:]))) if meals else 0

#     # plan_md = (
#     #     "### Week 1 (Base)\n"
#     #     f"- 3 easy runs: 20–30 min (RPE 3–4);\n"
#     #     "- 1 cross day: 30 min cycling or brisk walk\n"
#     #     f"- Protein target: PROTIEN g/day\n"
#     #     + (f"\n**Goal:** {goal}\n" if goal else "")
#     # )

#     return email

@mcp.tool
def whoami_link_account(pokeUserId: str, siteUserHandle: str):
    """
    Link the current Poke user to an OurSite user handle so future tools can omit userHandle.
    Use when user says: "link my account", "use my site profile", etc.
    Inputs:
      - pokeUserId: Poke's stable user identifier
      - siteUserHandle: user's handle on OurSite
    """
    # Store mapping in your DB; here we simulate success
    return {"ok": True, "msg": f"Linked {pokeUserId} → {siteUserHandle}"}



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    host = "0.0.0.0"
    
    print(f"Starting FastMCP server on {host}:{port}")
    
    mcp.run(
        transport="http",
        host=host,
        port=port
    )
