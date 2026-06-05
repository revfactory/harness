#!/usr/bin/env python3
"""Simple harness runner: loads a JSON config and executes agent callables.

Usage: python3 harness/harness.py --config harness/config/agents.json
"""
import argparse
import importlib
import json
import os
import sys
import traceback
from datetime import datetime

# Ensure the project root is on sys.path so `import harness.agents...` works
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# logging will be initialized after parsing CLI args
from harness.logging_setup import init_logging
logger = None


def load_config(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def call_agent(agent_conf, payload):
    module_name = agent_conf.get("module")
    callable_name = agent_conf.get("callable")
    params = agent_conf.get("params", {})
    module = importlib.import_module(module_name)
    func = getattr(module, callable_name)
    start = datetime.utcnow().isoformat() + "Z"
    logger.info("Calling agent %s.%s", module_name, callable_name)
    try:
        result = func(params, payload)
        end = datetime.utcnow().isoformat() + "Z"
        logger.info("Agent %s finished", agent_conf.get("name"))
        return {"agent": agent_conf.get("name"), "start": start, "end": end, "result": result}
    except Exception as e:
        end = datetime.utcnow().isoformat() + "Z"
        tb = traceback.format_exc()
        logger.exception("Agent %s raised exception", agent_conf.get("name"))
        return {
            "agent": agent_conf.get("name"),
            "start": start,
            "end": end,
            "error": {"message": str(e), "type": e.__class__.__name__, "traceback": tb},
        }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--config", required=False, help="path to agents config JSON")
    p.add_argument("--log-file", required=False, help="path to log file (append)")
    p.add_argument("--log-level", required=False, default=None, help="logging level, e.g. DEBUG, INFO, WARNING")
    p.add_argument("--log-max-bytes", required=False, type=int, default=None, help="max bytes for rotating log (0 disables rotation)")
    p.add_argument("--log-backup-count", required=False, type=int, default=None, help="number of rotated backup files to keep")
    p.add_argument("--defaults", required=False, help="path to defaults JSON (overrides harness/config/harness_defaults.json)")
    args = p.parse_args()

    # load defaults from file (bundle defaults live in harness/config)
    defaults_path = args.defaults or os.path.join(os.path.dirname(__file__), "config", "harness_defaults.json")
    defaults = {}
    if os.path.exists(defaults_path):
        try:
            defaults = load_config(defaults_path)
        except Exception:
            # fall back to empty defaults
            defaults = {}

    # resolve config path: CLI > defaults > error
    config_path = args.config or defaults.get("agents_config")
    if not config_path:
        raise SystemExit("No agents config provided (use --config or set agents_config in defaults)")

    # resolve logging options: CLI values override defaults
    resolved_log_file = args.log_file if args.log_file is not None else defaults.get("logging", {}).get("log_file")
    resolved_log_level = (args.log_level or defaults.get("logging", {}).get("log_level", "INFO")).upper()
    resolved_max_bytes = args.log_max_bytes if args.log_max_bytes not in (None, 0) else defaults.get("logging", {}).get("log_max_bytes", 0)
    resolved_backup_count = args.log_backup_count if args.log_backup_count not in (None, 0) else defaults.get("logging", {}).get("log_backup_count", 0)

    # initialize logging according to resolved values
    try:
        lvl = getattr(__import__("logging"), resolved_log_level)
    except Exception:
        lvl = getattr(__import__("logging"), "INFO")
    global logger
    logger = init_logging(level=lvl, logfile=resolved_log_file, max_bytes=resolved_max_bytes or 0, backup_count=resolved_backup_count or 0)

    if config_path:
        conf = load_config(config_path)
    else:
        # support embedding agents directly in defaults under key 'agents'
        conf = defaults.get("agents") or {}
    agents = conf.get("agents", [])

    # initial payload
    payload = {"id": "task-1", "payload": {"repo": "./"}, "history": []}

    for a in agents:
        print(f"Running agent: {a.get('name')}")
        out = call_agent(a, payload)
        payload["history"].append(out)
        # optionally pass the last result as the new payload
        payload["payload"][a.get("name")] = out.get("result")

    print("\nRun complete. History:")
    print(json.dumps(payload["history"], indent=2))


if __name__ == "__main__":
    main()
