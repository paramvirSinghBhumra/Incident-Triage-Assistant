# AI Incident Triage Assistant — Build Roadmap

Mentor-mode plan. Each milestone: what you're learning, what you build, how we check it before moving on. I won't write the working logic for you — I'll scaffold structure, explain concepts, review your code, and unblock you when stuck.

## Milestone 0 — Environment
- Install/configure AWS CLI + credentials locally (I can't reach your AWS account from here).
- Install AWS SAM CLI (simplest path to Lambda + API Gateway without hand-rolling IaC).
- Confirm you have Bedrock model access enabled for Claude Haiku in your AWS region (this requires a manual "request access" step in the Bedrock console the first time).
- **Check:** `aws sts get-caller-identity` works, `sam --version` works, Bedrock shows Haiku as "Access granted."

## Milestone 1 — Skeleton Lambda + API Gateway
- Concepts: event-driven Lambda, API Gateway proxy integration, IAM execution roles.
- Build: deploy the stubbed `template.yaml` in this folder as-is (it defines the API Gateway → Lambda wiring, nothing smart yet). Handler just logs the incoming event and returns 200.
- **Check:** `curl` or Postman a fake POST to your API Gateway URL, confirm CloudWatch Logs shows the payload.

## Milestone 2 — Parse the Datadog webhook
- Concepts: Datadog webhook payload shape, defensive parsing.
- Build: fill in `parse_alert()` in `handler.py` — extract alert name, monitor id, affected service/tag, time window.
- **Check:** unit test with a sample Datadog payload (I'll help you find/construct one) asserting the parsed fields.

## Milestone 3 — Datadog Logs API enrichment
- Concepts: scoping a log query by service + time window, API auth (Datadog API/App keys), controlling result size for token budget.
- Build: fill in `fetch_logs()`.
- **Check:** call it against a real (or sandbox) Datadog org, confirm you get back a bounded, relevant log slice — not everything.

## Milestone 4 — Bedrock + Claude Haiku call
- Concepts: `bedrock-runtime` invoke_model, prompt design for strict JSON output, IAM permissions for Bedrock, handling malformed/nondeterministic responses.
- Build: fill in `analyze()` — construct the prompt, call Haiku, validate/parse JSON, retry once on failure.
- **Check:** feed it a synthetic alert + log snippet, confirm you get valid JSON with severity/root cause/services/action every time across ~10 runs.

## Milestone 5 — Slack Block Kit output
- Concepts: incoming webhooks vs Slack apps, Block Kit JSON structure, color-coded attachments.
- Build: fill in `post_to_slack()`.
- **Check:** a real message lands in a test Slack channel, formatted and color-coded by severity, linking back to the monitor.

## Milestone 6 — Wire a real Datadog monitor
- Concepts: Datadog webhook notification channels, `@webhook-name` in monitor messages.
- Build: point a real (or test) Datadog monitor at your API Gateway URL.
- **Check:** trigger the monitor for real, watch the full path fire end-to-end within seconds.

## Milestone 7 — Hardening (optional but recommended)
- Idempotency (Datadog can retry webhooks), timeout/error handling per external call, cost guardrails (max tokens, log query size caps), structured logging for your own observability.

---
Current status: **Milestone 0** — nothing deployed yet. Scaffold for Milestone 1 is in this folder (`template.yaml`, `handler.py`, `requirements.txt`).
