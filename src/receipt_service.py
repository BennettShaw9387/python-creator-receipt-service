from __future__ import annotations

from dataclasses import dataclass

from .infrai_client import EmailResult, InfraiEmail


@dataclass(frozen=True)
class Order:
    order_id: str
    buyer_email: str
    buyer_name: str
    asset_name: str
    download_url: str
    amount_cents: int
    subscriber_updates: bool = True


def render_receipt(order: Order) -> str:
    amount = f"${order.amount_cents / 100:.2f}"
    update_note = " You are subscribed to delivery updates." if order.subscriber_updates else ""
    return (
        f"<h1>Receipt for order {order.order_id}</h1>"
        f"<p>Hi {order.buyer_name}, your {order.asset_name} is ready.</p>"
        f"<p>Total: <strong>{amount}</strong>.</p>"
        f"<p><a href=\"{order.download_url}\">Download your files</a>.</p>"
        f"<p>{update_note}</p>"
    )


def send_order_receipt(order: Order, email: InfraiEmail | None = None) -> EmailResult:
    client = email or InfraiEmail()
    # The public call shape is infrai.email.send(...); this wrapper keeps the order decision visible.
    return client.send(
        {
            "to": order.buyer_email,
            "subject": f"Receipt {order.order_id}: {order.asset_name}",
            "html": render_receipt(order),
        },
        request_id=f"receipt-{order.order_id}",
    )


def delivery_snapshot(message_id: str, email: InfraiEmail | None = None) -> dict:
    return (email or InfraiEmail()).events(message_id)
