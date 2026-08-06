"""
AI Incident Triage Assistant — Lambda entry point.

Mentor-mode scaffold: the pipeline shape is here, the logic isn't.
Fill in each TODO in order (see ../ROADMAP.md for the milestone that
matches each function). Don't skip ahead — each step is independently
testable before you wire it to the next.
"""

import json
import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    """
    API Gateway proxy entry point. `event` is the API Gateway event envelope;
    the Datadog webhook JSON body is in event["body"] as a string.
    """
    logger.info("Received event: %s", json.dumps(event))

    try:
        alert = parse_alert(event)
    except Exception:
        logger.exception("Failed to parse alert payload")
        return _response(400, {"error": "invalid payload"})

    logs = fetch_logs(alert)
    analysis = analyze(alert, logs)
    post_to_slack(alert, analysis)

    return _response(200, {"status": "ok"})


def parse_alert(event):
    """
    Milestone 2.
    Parse the Datadog webhook payload out of `event["body"]`.

    Return a dict with at least:
      - alert_name: str
      - monitor_id: str
      - service: str            (which service/tag the alert is about)
      - monitor_url: str         (link back to Datadog, for the Slack message)
      - window_start / window_end: for scoping the log query in Milestone 3

    Datadog's webhook payload includes fields like $EVENT_TITLE, $ID,
    $ALERT_TRANSITION, tags, etc. — the exact keys depend on how you template
    the webhook payload in the Datadog notification channel config. Decide
    that payload shape together with this function.
    """
    raise NotImplementedError("Milestone 2: parse the Datadog webhook payload")


def fetch_logs(alert):
    """
    Milestone 3.
    Query the Datadog Logs API (https://docs.datadoghq.com/api/latest/logs/)
    for recent log lines scoped to `alert["service"]` and the alert's time
    window. Keep the query tight — this feeds directly into the LLM prompt,
    so an unbounded query means unbounded token cost.

    Return a short string or list of log lines, not the raw API response.
    """
    raise NotImplementedError("Milestone 3: fetch scoped log context from Datadog")


def analyze(alert, logs):
    """
    Milestone 4.
    Call Claude Haiku via Bedrock's `bedrock-runtime` `invoke_model` API.
    Prompt it to return ONLY a JSON object with:
      - severity: "P1" | "P2" | "P3"
      - root_cause: str (one sentence)
      - affected_services: list[str]
      - suggested_action: str

    Parse and validate the response. If it's not valid JSON or is missing
    fields, retry once with a stricter instruction before giving up.
    """
    raise NotImplementedError("Milestone 4: call Bedrock and get structured JSON back")


def post_to_slack(alert, analysis):
    """
    Milestone 5.
    Render `analysis` as a Slack Block Kit message (color-coded by severity)
    and POST it to the incoming webhook URL in SLACK_WEBHOOK_URL. Include a
    link back to alert["monitor_url"].
    """
    raise NotImplementedError("Milestone 5: post a Block Kit message to Slack")


def _response(status_code, body):
    return {
        "statusCode": status_code,
        "body": json.dumps(body),
    }
