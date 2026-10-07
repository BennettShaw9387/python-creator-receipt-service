from src.receipt_service import Order, render_receipt, send_order_receipt


class FakeEmail:
    def __init__(self):
        self.payload = None

    def send(self, payload, request_id):
        self.payload = (payload, request_id)
        return type("Result", (), {"message_id": "msg-test"})()


def test_receipt_contains_asset_link_and_subscriber_note():
    order = Order("o-1", "buyer@example.com", "Mina", "Lightroom presets", "https://x.test/o-1", 1250)
    fake = FakeEmail()
    result = send_order_receipt(order, fake)
    payload, request_id = fake.payload
    assert result.message_id == "msg-test"
    assert request_id == "receipt-o-1"
    assert "https://x.test/o-1" in payload["html"]
    assert "subscribed to delivery updates" in payload["html"]
    assert payload["subject"] == "Receipt o-1: Lightroom presets"

