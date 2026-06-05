Minimal Harness for revfactory/harness

Quick start

1. Run the harness:

```bash
python3 harness/harness.py --config harness/config/agents.json
```

What this does

- Loads `harness/config/agents.json` which declares the agent team and simple parameters.
- Dynamically imports example agent modules from `harness/agents/` and calls their `run(config)` function.

Next steps

- Replace or extend the example agents in `harness/agents/` with real implementations.
- Hook the harness into CI or orchestration for automated runs.
