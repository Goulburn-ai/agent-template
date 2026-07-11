# {{cookiecutter.agent_name}}

![goulburn trust](https://api.goulburn.ai/api/v1/agents/{{cookiecutter.agent_name}}/badge.svg)

> {{cookiecutter.agent_description}}

**Trust verification by [goulburn.ai](https://goulburn.ai). Your code. Our trust layer.**

## Quick start

```bash
pip install -e .
export GEMINI_API_KEY=your-key   # never commit this
python agent.py                  # runs on http://localhost:8000
```

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
