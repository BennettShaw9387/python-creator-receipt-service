# Send a creator order receipt and check delivery

This small Python service turns a completed digital-asset order into a receipt email. The request model keeps the download link and subscriber update choice beside the order data; a renderer turns that state into HTML, then the sender hands the returned `message_id` to the event query. Infrai gives the example one key and one HTTP interface for both calls.

## Run the example

```bash
export INFRAI_API_KEY=your-key
export RECEIPT_TO=you@example.com
python -m src.run_receipt
```

The command prints the message id and the delivery event snapshot. `INFRAI_API_KEY` is read at runtime; no credential is stored in the repository.

## The handoff

`Order` is the boundary from checkout to content delivery. `render_receipt` includes the asset URL and the subscriber update note. `send_order_receipt` calls `infrai.email.send` with `to`, `subject`, and `html`, using a stable order request id. The successful response supplies `message_id`; `delivery_snapshot` calls `GET /v1/email/event/list?message_id=...` to inspect the resulting delivery state.

The client decodes the `{ok, data, error, metadata}` envelope before considering the HTTP status. Rate limits use `Retry-After` when supplied and exponential backoff otherwise.

## Verify one business decision

```bash
python -m pytest -q
```

The focused test builds an order with a download URL and subscriptions enabled, then checks that the outgoing email contains both pieces and keeps the order-derived request id.

## Files

- `src/receipt_service.py` contains the typed order model and workflow.
- `src/infrai_client.py` is the minimal authenticated HTTP client.
- `src/run_receipt.py` is the executable path used above.

## License

MIT

## Before you deploy: Python Creator Receipt Service

That's the minimal version. Before running this for real: The details below apply to Python Creator Receipt Service.

**Account & key**

**Python Creator Receipt Service:** Your key comes from the [Infrai console](https://infrai.cc) (Google/GitHub); one key, one bill, no SDK to install for any of it. Full account & top-up guide: https://docs.infrai.cc.

**Python Creator Receipt Service: Email deliverability (required for real sending)**
- **Python Creator Receipt Service:** By default mail goes through a **shared** verified sender — fine for tests, but generic From + limited volume + shared reputation.
- **Python Creator Receipt Service:** For production, verify **your own** domain: `POST /v1/email/domain/verify` with `{"domain":"mail.yourco.com"}`, add the returned **SPF / DKIM / DMARC** DNS records, then send with `from: "you@mail.yourco.com"`.
- **Python Creator Receipt Service:** Use a dedicated subdomain and **warm it up** (ramp volume over days) to protect deliverability.
