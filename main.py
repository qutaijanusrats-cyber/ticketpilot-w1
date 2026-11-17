import os, json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "openai/gpt-oss-20b"
ORDERS = {
    "A123": {"status": "Shipped", "eta": "2 days"},
    "A124": {"status": "Processing", "eta": "5 days"},
    "A125": {"status": "Delivered", "eta": None},
    "A126": {"status": "Cancelled", "eta": None},
    "A127": {"status": "Out for delivery", "eta": "today"},
}

def lookup_order_status(order_id: str) -> dict:
    return ORDERS.get(order_id.upper(), {"error": "not found"})

tools = [{
    "type": "function",
    "function": {
        "name": "lookup_order_status",
        "description": "Look up the current shipping status of an order by its ID",
        "parameters": {
            "type": "object",
            "properties": {"order_id": {"type": "string", "description": "e.g. A123"}},
            "required": ["order_id"],
        },
    },
}]

messages = [{"role": "user", "content": input("Ask: ")}]
resp = client.chat.completions.create(model=MODEL, messages=messages, tools=tools)
msg = resp.choices[0].message
print("RAW TOOL CALL:", msg.tool_calls)  # needed for the "done when" check

if msg.tool_calls:
    messages.append(msg)
    for call in msg.tool_calls:
        args = json.loads(call.function.arguments)
        result = lookup_order_status(**args)
        messages.append({"role": "tool", "tool_call_id": call.id,
                         "content": json.dumps(result)})
    final = client.chat.completions.create(model=MODEL, messages=messages, tools=tools)
    print("ANSWER:", final.choices[0].message.content)
else:
    print("ANSWER:", msg.content)