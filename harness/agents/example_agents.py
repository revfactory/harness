
"""Example agent implementations used by the harness for demonstration.

Each callable accepts `(params, input_payload)` and returns a serializable result.
"""
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def orchestrator(params, input_payload):
    logger.debug("orchestrator start")
    return {"note": "orchestrator started", "timestamp": datetime.utcnow().isoformat()}


def scout(params, input_payload):
    logger.debug("scout start params=%s", params)
    seed = params.get("seed", "unknown")
    discovered = {"repos": ["/workspaces/harness"], "seed": seed}
    logger.debug("scout discovered=%s", discovered)
    return {"discovered": discovered, "timestamp": datetime.utcnow().isoformat()}


def auditor(params, input_payload):
    logger.debug("auditor start")
    issues = []
    if "harness" in input_payload.get("payload", {}).get("repo", ""):
        issues.append({"type": "info", "message": "harness folder present"})
    logger.debug("auditor issues=%s", issues)
    return {"issues": issues, "timestamp": datetime.utcnow().isoformat()}


def strategist(params, input_payload):
    logger.debug("strategist start")
    plan = ["audit", "generate_content", "qa"]
    return {"plan": plan, "timestamp": datetime.utcnow().isoformat()}


def content_generator(params, input_payload):
    logger.debug("content_generator start")
    summary = "Generated summary for task"
    return {"summary": summary, "timestamp": datetime.utcnow().isoformat()}


def qa(params, input_payload):
    logger.debug("qa start")
    ok = True
    return {"ok": ok, "notes": [], "timestamp": datetime.utcnow().isoformat()}
