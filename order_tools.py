MOCK_ORDERS = {
    "ORD-123": {
        "status": "Shipped",
        "carrier": "PostNord",
        "estimated_delivery": "12 August 2026",
    },
    "ORD-456": {
        "status": "Processing",
        "carrier": None,
        "estimated_delivery": "15 August 2026",
    },
}

def check_order_status(order_number):
    order_number = order_number.strip().upper()
    order = MOCK_ORDERS.get(order_number)

    if not order:
        return None

    return order