import re
import json

def parse_tool_response(response_message):
    if re.match(r"```tool", response_message):
        try:
            tool_response = re.split(r'```(tool)?', response_message)[2].strip()
            return json.loads(tool_response)
        except Exception as e:
            print(f"Error parsing tool response: {e}")
            print(response_message)
            return "Invalid tool call."
    else:
        print('No tool response found in the message.')
        return "Unable to process response. No tool response found in message."

def print_tool_message(tool_response):
    if type(tool_response) is str:
        return "Cannot parse message."
    
    if tool_response and tool_response.get("message"):
        print(f"Agent: {tool_response.get('message')}")
    elif tool_response and tool_response.get("description"):
        print(f"Agent: {tool_response.get('description')}")