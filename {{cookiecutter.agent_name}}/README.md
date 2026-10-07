# {{cookiecutter.agent_name}}

![goulburn trust](https://api.goulburn.ai/api/v1/agents/{{cookiecutter.agent_name}}/badge.svg)

> {{cookiecutter.agent_description}}

**Trust verification by [goulburn.ai](https://goulburn.ai). Your code. Our trust layer.**

## Quick start

```bash
pip install -e .
export GEMINI_API_KEY=your-key   # never commit this
python agent.py                  # runs on http://127.0.0.1:8000
```

Before exposing `/chat` beyond your machine, set `AGENT_SHARED_SECRET`. Without
it, anyone who can reach the port spends your `GEMINI_API_KEY`.

| Variable | Default | Effect |
|---|---|---|
| `AGENT_SHARED_SECRET` | unset | When set, `/chat` requires `Authorization: Bearer <secret>` |
| `HOST` / `PORT` | `127.0.0.1` / `8000` | Bind address for `python agent.py` |
| `RATE_LIMIT_PER_MIN` | `30` | Requests per client IP per minute, `0` turns it off |

Requests are capped at 64 KB, 50 messages and 8,000 characters per message.
Run the tests with `pip install -e ".[dev]" && pytest`.

## CI trust gate

Every push to `main` runs [goulburn-trust-check](https://github.com/Goulburn-ai/trust-check). Deploys fail if the agent's trust score drops below {{cookiecutter.trust_threshold}}.

Add `GOULBURN_API_KEY` to your repo's Settings > Secrets > Actions.

## Self-hosted probes

```bash
pip install goulburn-probe-runner
goulburn-probe-runner run --config probes.yml --api-key $GOULBURN_API_KEY
```

## Architecture

- `agent.yaml`: agent config + system prompt (review before making repo public)
- `agent.py`: FastAPI /chat handler calling {{cookiecutter.model}}
- `probes.yml`: 6 built-in probes for goulburn-probe-runner
- `.github/workflows/trust-gate.yml`: CI trust-check (gates on score + tier)
