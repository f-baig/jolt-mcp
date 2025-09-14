#!/usr/bin/env python3
import os
import json
import requests
from fastmcp import FastMCP
from dotenv import load_dotenv

load_dotenv()

mcp = FastMCP("jolt-mcp")

# Base URL for your Flask API
API_BASE_URL = os.getenv("API_BASE_URL", "https://jolt.nikhilrado.com")

def make_api_request(endpoint: str, user_api_token: str, method: str = "GET", data: dict = None) -> dict:
    """Helper function to make authenticated API requests"""
    headers = {"Authorization": f"Bearer {user_api_token}"}
    url = f"{API_BASE_URL}{endpoint}"
    
    print(f"Making {method} request to {url}")
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=10)
        elif method == "POST":
            headers["Content-Type"] = "application/json"
            response = requests.post(url, headers=headers, json=data, timeout=10)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers, timeout=10)
        else:
            return {"error": f"Unsupported HTTP method: {method}"}
        
        print(f"API response status: {response.status_code}")
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"API request failed: {response.text}")
            return {"error": f"API request failed with status {response.status_code}", "details": response.text}
            
    except Exception as e:
        print(f"Error in API request: {str(e)}")
        return {"error": f"Request failed: {str(e)}"}

# ============================================================================
# USER PROFILE & AUTHENTICATION TOOLS
# ============================================================================

@mcp.tool(description="Get user profile information including ID and token status.")
def get_user_profile(user_api_token: str) -> dict:
    """
    Get user profile information using their API token.
    Returns user ID, token validity, and basic profile data.
    """
    print(f"get_user_profile called with token: {user_api_token[:10]}...")
    return make_api_request("/api/v1/profile", user_api_token)

@mcp.tool(description="Get user's email address or user ID information.")
def get_user_email(user_api_token: str) -> dict:
    """
    Get user's email address using their API token.
    Note: This may return user ID if email retrieval is not fully implemented.
    """
    print(f"get_user_email called with token: {user_api_token[:10]}...")
    return make_api_request("/api/v1/email", user_api_token)

@mcp.tool(description="Get current API token status and information.")
def get_token_status(user_api_token: str) -> dict:
    """
    Get information about the current API token including creation date, expiration, and usage.
    """
    print(f"get_token_status called with token: {user_api_token[:10]}...")
    return make_api_request("/api/v1/token", user_api_token)

# ============================================================================
# STRAVA ACTIVITIES & FITNESS TOOLS
# ============================================================================

@mcp.tool(description="Get user's Strava activities and workout data.")
def get_strava_activities(user_api_token: str) -> dict:
    """
    Get user's Strava activities using their API token.
    Requires Strava account to be connected.
    """
    print(f"get_strava_activities called with token: {user_api_token[:10]}...")
    return make_api_request("/api/strava/activities", user_api_token)

@mcp.tool(description="Get user's running and fitness statistics.")
def get_fitness_stats(user_api_token: str) -> dict:
    """
    Get comprehensive fitness statistics including total runs, distance, time, and average pace.
    """
    print(f"get_fitness_stats called with token: {user_api_token[:10]}...")
    return make_api_request("/api/v1/stats", user_api_token)

@mcp.tool(description="Get Strava connection status and webhook information.")
def get_strava_status(user_api_token: str) -> dict:
    """
    Check if user's Strava account is connected and get connection status.
    """
    print(f"get_strava_status called with token: {user_api_token[:10]}...")
    return make_api_request("/api/strava/status", user_api_token)

# ============================================================================
# ANALYTICS & PERFORMANCE TOOLS
# ============================================================================

@mcp.tool(description="Get comprehensive training analytics and insights.")
def get_comprehensive_analytics(user_api_token: str, days: int = 90) -> dict:
    """
    Get comprehensive training analytics including training load, intensity zones, 
    performance curves, volume trends, and consistency metrics.
    
    Args:
        user_api_token: User's API token
        days: Analysis period in days (7, 14, 30, 60, 90, 180, 365)
    """
    print(f"get_comprehensive_analytics called with token: {user_api_token[:10]}..., days: {days}")
    return make_api_request(f"/api/analytics/comprehensive?days={days}", user_api_token)

@mcp.tool(description="Get training analytics summary with key metrics.")
def get_analytics_summary(user_api_token: str) -> dict:
    """
    Get a summary of training analytics with key performance metrics.
    """
    print(f"get_analytics_summary called with token: {user_api_token[:10]}...")
    return make_api_request("/api/analytics/summary", user_api_token)

@mcp.tool(description="Get performance trends and progression data.")
def get_performance_trends(user_api_token: str) -> dict:
    """
    Get performance trends showing progression over time.
    """
    print(f"get_performance_trends called with token: {user_api_token[:10]}...")
    return make_api_request("/api/analytics/performance-trends", user_api_token)

# ============================================================================
# PSYCHOLOGY & WELLNESS TOOLS
# ============================================================================

@mcp.tool(description="Get psychological analysis of training performance.")
def get_psychology_analysis(user_api_token: str) -> dict:
    """
    Get psychological analysis of training performance and mental state.
    """
    print(f"get_psychology_analysis called with token: {user_api_token[:10]}...")
    return make_api_request("/api/psychology/analysis", user_api_token)

@mcp.tool(description="Get performance events and psychological insights.")
def get_performance_events(user_api_token: str) -> dict:
    """
    Get analysis of performance events and their psychological impact.
    """
    print(f"get_performance_events called with token: {user_api_token[:10]}...")
    return make_api_request("/api/psychology/performance-events", user_api_token)

@mcp.tool(description="Get split analysis for a specific activity.")
def get_split_analysis(user_api_token: str, activity_id: int) -> dict:
    """
    Get detailed split analysis for a specific Strava activity.
    
    Args:
        user_api_token: User's API token
        activity_id: Strava activity ID to analyze
    """
    print(f"get_split_analysis called with token: {user_api_token[:10]}..., activity_id: {activity_id}")
    return make_api_request(f"/api/psychology/split-analysis/{activity_id}", user_api_token)

@mcp.tool(description="Get psychological insights and recommendations.")
def get_psychology_insights(user_api_token: str) -> dict:
    """
    Get psychological insights and mental performance recommendations.
    """
    print(f"get_psychology_insights called with token: {user_api_token[:10]}...")
    return make_api_request("/api/psychology/insights", user_api_token)

@mcp.tool(description="Submit wellness data and feelings.")
def submit_wellness_data(user_api_token: str, wellness_data: dict) -> dict:
    """
    Submit wellness data including mood, energy, sleep quality, etc.
    
    Args:
        user_api_token: User's API token
        wellness_data: Dictionary containing wellness metrics
    """
    print(f"submit_wellness_data called with token: {user_api_token[:10]}...")
    return make_api_request("/api/psychology/submit-wellness", user_api_token, "POST", wellness_data)

@mcp.tool(description="Analyze feelings and emotional state from text.")
def analyze_feelings(user_api_token: str, feelings_text: str) -> dict:
    """
    Analyze feelings and emotional state from provided text.
    
    Args:
        user_api_token: User's API token
        feelings_text: Text describing feelings or emotional state
    """
    print(f"analyze_feelings called with token: {user_api_token[:10]}...")
    data = {"feelings_text": feelings_text}
    return make_api_request("/api/psychology/analyze-feelings", user_api_token, "POST", data)

# ============================================================================
# NUTRITION TOOLS
# ============================================================================

@mcp.tool(description="Get nutrition dashboard with trends and averages.")
def get_nutrition_dashboard(user_api_token: str, days: int = 7) -> dict:
    """
    Get nutrition dashboard data including trends, averages, and daily summaries.
    
    Args:
        user_api_token: User's API token
        days: Analysis period in days (1, 3, 7, 14, 30)
    """
    print(f"get_nutrition_dashboard called with token: {user_api_token[:10]}..., days: {days}")
    return make_api_request(f"/api/nutrition/dashboard?days={days}", user_api_token)

@mcp.tool(description="Get comprehensive nutrition insights and analysis.")
def get_nutrition_insights(user_api_token: str, days: int = 30) -> dict:
    """
    Get comprehensive nutrition insights including patterns, recommendations, and analysis.
    
    Args:
        user_api_token: User's API token
        days: Analysis period in days (7, 14, 30, 60, 90)
    """
    print(f"get_nutrition_insights called with token: {user_api_token[:10]}..., days: {days}")
    return make_api_request(f"/api/nutrition/insights?days={days}", user_api_token)

@mcp.tool(description="Log a meal with nutritional information.")
def log_meal(user_api_token: str, meal_data: dict) -> dict:
    """
    Log a meal with nutritional information.
    
    Args:
        user_api_token: User's API token
        meal_data: Dictionary containing meal information (name, calories, macros, etc.)
    """
    print(f"log_meal called with token: {user_api_token[:10]}...")
    return make_api_request("/api/nutrition/log-meal", user_api_token, "POST", meal_data)

@mcp.tool(description="Get daily nutrition summary.")
def get_daily_nutrition_summary(user_api_token: str) -> dict:
    """
    Get daily nutrition summary with totals and breakdowns.
    """
    print(f"get_daily_nutrition_summary called with token: {user_api_token[:10]}...")
    return make_api_request("/api/nutrition/daily-summary", user_api_token)

@mcp.tool(description="Get nutrition trends over time.")
def get_nutrition_trends(user_api_token: str) -> dict:
    """
    Get nutrition trends showing changes in eating patterns over time.
    """
    print(f"get_nutrition_trends called with token: {user_api_token[:10]}...")
    return make_api_request("/api/nutrition/trends", user_api_token)

@mcp.tool(description="Get nutrition patterns and eating behavior analysis.")
def get_nutrition_patterns(user_api_token: str) -> dict:
    """
    Get nutrition patterns and eating behavior analysis.
    """
    print(f"get_nutrition_patterns called with token: {user_api_token[:10]}...")
    return make_api_request("/api/nutrition/patterns", user_api_token)

# ============================================================================
# MCP-SPECIFIC NUTRITION TOOLS (CalorieNinjas Integration)
# ============================================================================

@mcp.tool(description="Analyze meal description using CalorieNinjas API.")
def analyze_meal_description(meal_description: str) -> dict:
    """
    Analyze a meal description using CalorieNinjas API to get nutritional information.
    This tool doesn't require authentication as it's a public analysis service.
    
    Args:
        meal_description: Text description of the meal to analyze
    """
    print(f"analyze_meal_description called with description: {meal_description[:50]}...")
    data = {"meal_description": meal_description}
    return make_api_request("/api/mcp/nutrition/analyze", "", "POST", data)

@mcp.tool(description="Analyze meal description and save to user's nutrition log.")
def analyze_and_save_meal(user_api_token: str, meal_description: str) -> dict:
    """
    Analyze a meal description and save the results to the user's nutrition log.
    
    Args:
        user_api_token: User's API token
        meal_description: Text description of the meal to analyze and save
    """
    print(f"analyze_and_save_meal called with token: {user_api_token[:10]}...")
    data = {"meal_description": meal_description}
    return make_api_request("/api/mcp/nutrition/analyze-and-save", user_api_token, "POST", data)

@mcp.tool(description="Analyze multiple meal descriptions in batch.")
def batch_analyze_meals(meal_descriptions: list) -> dict:
    """
    Analyze multiple meal descriptions in a single batch request.
    
    Args:
        meal_descriptions: List of meal description strings to analyze
    """
    print(f"batch_analyze_meals called with {len(meal_descriptions)} meals")
    data = {"meal_descriptions": meal_descriptions}
    return make_api_request("/api/mcp/nutrition/batch-analyze", "", "POST", data)

@mcp.tool(description="Get health recommendations based on nutritional data.")
def get_health_recommendations(user_api_token: str, nutritional_data: dict = None) -> dict:
    """
    Get personalized health recommendations based on nutritional data.
    
    Args:
        user_api_token: User's API token
        nutritional_data: Optional nutritional data to analyze (if not provided, uses user's recent data)
    """
    print(f"get_health_recommendations called with token: {user_api_token[:10]}...")
    data = nutritional_data or {}
    return make_api_request("/api/mcp/nutrition/health-recommendations", user_api_token, "POST", data)

# ============================================================================
# NOTIFICATION TOOLS
# ============================================================================

@mcp.tool(description="Get Strava notifications and updates.")
def get_strava_notifications(user_api_token: str) -> dict:
    """
    Get Strava notifications and recent updates.
    """
    print(f"get_strava_notifications called with token: {user_api_token[:10]}...")
    return make_api_request("/api/user/strava/notifications", user_api_token)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    
    print("=" * 60)
    print("Starting Jolt MCP Server")
    print(f"Host: {host}")
    print(f"Port: {port}")
    print(f"API Base URL: {API_BASE_URL}")
    print(f"Environment: {os.environ.get('ENVIRONMENT', 'development')}")
    print("=" * 60)
    print("Available MCP Tools:")
    print("USER PROFILE & AUTH:")
    print("  - get_user_profile")
    print("  - get_user_email") 
    print("  - get_token_status")
    print("STRAVA & FITNESS:")
    print("  - get_strava_activities")
    print("  - get_fitness_stats")
    print("  - get_strava_status")
    print("ANALYTICS & PERFORMANCE:")
    print("  - get_comprehensive_analytics")
    print("  - get_analytics_summary")
    print("  - get_performance_trends")
    print("PSYCHOLOGY & WELLNESS:")
    print("  - get_psychology_analysis")
    print("  - get_performance_events")
    print("  - get_split_analysis")
    print("  - get_psychology_insights")
    print("  - submit_wellness_data")
    print("  - analyze_feelings")
    print("NUTRITION:")
    print("  - get_nutrition_dashboard")
    print("  - get_nutrition_insights")
    print("  - log_meal")
    print("  - get_daily_nutrition_summary")
    print("  - get_nutrition_trends")
    print("  - get_nutrition_patterns")
    print("MCP NUTRITION (CalorieNinjas):")
    print("  - analyze_meal_description")
    print("  - analyze_and_save_meal")
    print("  - batch_analyze_meals")
    print("  - get_health_recommendations")
    print("NOTIFICATIONS:")
    print("  - get_strava_notifications")
    print("=" * 60)
    
    print(f"Starting FastMCP server on {host}:{port}")
    
    try:
        mcp.run(
            transport="http",
            host=host,
            port=port
        )
    except Exception as e:
        print(f"Failed to start MCP server: {str(e)}")
        raise