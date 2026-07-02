import re
import json

def parse_tool_response(response_message):
    if response_message.startswith("```tool"):
        try:
            tool_response = re.split(r'```(tool)?', response_message)[2].strip()
            return json.loads(tool_response)
        except Exception as e:
            print(f"Error parsing tool response: {e}")
            return None
    else:
        print(response_message)
        return None

def print_tool_message(tool_response):
    if tool_response and tool_response.get("message"):
        print(f"Agent: {tool_response.get('message')}")
        
    if tool_response and tool_response.get("description"):
        print(f"Agent: {tool_response.get('description')}")