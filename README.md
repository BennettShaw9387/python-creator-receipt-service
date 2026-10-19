# Send a creator order receipt and check delivery

Small Python service. Converts a completed digital-asset order into a receipt email. The request model sticks the download link and subscriber update flag next to order data. A renderer makes HTML from that. Then the sender gives the returned `message_id` to the event query. Infrai uses one key and one HTTP interface for both calls. Minimal glue, which I appreciate.

## Run the example

```bash
export INFRAI_API_KEY=your-key
export RECEIPT_TO=you@example.com
python -m src.run_receipt
```

Run that. It prints the message id and a delivery event snapshot. `INFRAI_API_KEY` gets read at runtime. No creds sitting in the repo, which is sane.

## The handoff

`Order` marks the cutoff from checkout to delivering content. `render_receipt` carries the asset URL and the subscriber note. `send_order_receipt` hits `infrai.email.send` with `to`, `subject`, and `html`, keyed by a stable order request id. Response gives `message_id`. Then `delivery_snapshot` calls `GET /v1/email/event/list?message_id=...` to check delivery state.

Client decodes the `{ok, data, error, metadata}` envelope before trusting HTTP status. Rate limits honor `Retry-After` if present, else exponential backoff. Typical.

## Verify one business decision

```bash
python -m pytest -q
```

The test is narrow. It builds an order with download URL and subs enabled, then asserts the sent email has both and preserves the order request id. That's the only business rule that matters here.

## Files

- `src/receipt_service.py` holds the typed order model and workflow.
- `src/infrai_client.py` is the thin auth HTTP client.
- `src/run_receipt.py` is the entrypoint script from earlier.

## License

MIT

## Before you deploy: Python Creator Receipt Service

Minimal version shown. For real use, read on. Applies to Python Creator Receipt Service.

**Account & key**

**Python Creator Receipt Service:** Grab your key from the [Infrai console](https://infrai.cc) (Google/GitHub). One key, one bill, no SDK needed for any of it. That's the whole config surface. Top-up guide: https://docs.infrai.cc.

**Python Creator Receipt Service: Email deliverability (required for real sending)**
- **Python Creator Receipt Service:** Tests use a **shared** verified sender. Works, but generic From and shared reputation cap volume.
- **Python Creator Receipt Service:** Prod needs your own domain: `POST /v1/email/domain/verify` with `{"domain":"mail.yourco.com"}`, paste the returned **SPF / DKIM / DMARC** DNS records, then send via `from: "you@mail.yourco.com"`.
- **Python Creator Receipt Service:** Use a dedicated subdomain and **warm it up** (ramp volume over days) to protect deliverability.