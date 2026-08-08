import os

from dotenv import load_dotenv
from openrouter import OpenRouter


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
        stream=False,
    )

    assistant_message = response.choices[0].message.content

    conversation.append(
        {
            "role": "assistant",
            "content": assistant_message,
        }
    )

    print("UrbanThread AI:", assistant_message)