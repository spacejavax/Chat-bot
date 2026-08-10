import os
import json
from dotenv import load_dotenv
from openrouter import OpenRouter
from order_tools import check_order_status


load_dotenv()

hackclub_key = os.getenv("HACKCLUB_AI_API_KEY")

if not hackclub_key:
    raise ValueError("The API key was not found in the .env file")


client = OpenRouter(
    api_key=hackclub_key, server_url="https://ai.hackclub.com/proxy/v1",
)

SYSTEM_PROMPT = """
You are UrbanThread's customer-support assistant.
UrbanThread is a fictional online clothing store.

You help customers with:
-order
-product availability
-returns and exchanges
-shippig
-order cancellations
-adress changes
-payment problems
-discounts
-damaged products
-contacting a human

Rules:
Be friendly, concise, and professional.
-Never invent order details, tracking information, or refund status.
-Ask for an order number when the question concerns a specific order.
-Never ask for passwords or complete payment-card information.
-Do not claim that you checked an order unless the program gives you order data.
-If you do not have enough information, clearly say so.
-If you cannot safely answer, offer to connect the customer with a human. 
"""

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "check_order_status",
            "description": "Look up a fictional UrbanThread order using its order number",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_number": {
                        "type": "string",
                        "description": "The customer order number, such as ORD-123",
                    }
                },
                "required": ["order_number"],
            },
        },
    }
]

conversation = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT,
    }
]
print("UrbanThread AI: Hi! How can I help you?")
print("Type quit when you want to end the conversation.")

while True:
    user_message = input("Type: ").strip()

    if user_message.lower() == "quit":
        print("UrbanThread AI: Goodbye!")
        break
    if not user_message: #true
        continue #back to input
    conversation.append(
        {
            "role": "user",
            "content": user_message,
        }
    )
    response = client.chat.send(
        model="qwen/qwen3-32b",
        messages=conversation,
        tools=TOOLS,
        stream=False,
    )

    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls

    if tool_calls:
        tool_call = tool_calls[0]

        arguments = json.loads(tool_call.function.arguments)
        order_number = arguments["order_number"]
        order_result = check_order_status(order_number)

        conversation.append(
            {
                "role": "assistant",
                "content": response_message.content,
                "tool_calls": [
                    {
                        "id": tool_call.id,
                        "type": "function",
                        "function": {
                            "name": tool_call.function.name,
                            "arguments": tool_call.function.arguments,
                        },
                    }
                ],
            }
        )

        conversation.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(order_result),
            }
        )

        final_response = client.chat.send(
            model="qwen/qwen3-32b",
            messages=conversation,
            tools=TOOLS,
            stream=False,
        )

        assistant_message = final_response.choices[0].message.content

    else:
        assistant_message = response_message.content   

    conversation.append(
        {
            "role": "assistant",
            "content": assistant_message,
        }
    )
    print("UrbanThread AI:", assistant_message)