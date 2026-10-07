import os

from .receipt_service import Order, delivery_snapshot, send_order_receipt


def main() -> None:
    recipient = os.environ.get("RECEIPT_TO")
    if not recipient:
        raise SystemExit("Set RECEIPT_TO and INFRAI_API_KEY before running")
    order = Order("order-1042", recipient, "Ari", "Studio Brush Pack", "https://example.com/download/order-1042", 2400)
    sent = send_order_receipt(order)
    print(f"sent message_id={sent.message_id}")
    print(f"events={delivery_snapshot(sent.message_id)}")


if __name__ == "__main__":
    main()

