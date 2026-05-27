# goulburn.ai agent template

Cookiecutter template for bootstrapping a goulburn.ai-verified AI agent.

## Usage

```bash
pip install cookiecutter
cookiecutter gh:goulburn-ai/agent-template
```

You'll be prompted for:
- **agent_name** — your goulburn.ai agent name
- **agent_description** — one-line description
- **system_prompt** — the LLM system prompt
- **provider** — LLM provider (default: google)
- **model** — model identifier (default: gemini-2.5-flash-lite)
- **trust_threshold** — minimum trust score to pass CI (default: 60)
- **required_tier** — minimum tier to pass CI (default: verified)
- **capability_tags** — comma-separated tags

## What you get

```
my-agent/
├── agent.yaml           # config + system prompt
├── agent.py             # FastAPI /chat handler (~55 LOC)
├── probes.yml           # goulburn-probe-runner config (6 built-in probes)
├── README.md            # trust badge + quick start
├── pyproject.toml       # pinned dependencies
├── .gitignore           # .env + caches
└── .github/workflows/
    └── trust-gate.yml   # CI trust-check via goulburn-ai/trust-check@v1
```

## Learn more

- [goulburn.ai](https://goulburn.ai) — trust verification for AI agents
- [trust-check](https://github.com/Goulburn-ai/trust-check) — CI gate GitHub Action
- [probe-runner](https://github.com/Goulburn-ai/goulburn-probe-runner) — self-hosted probe CLI
- [Python SDK](https://pypi.org/project/goulburn/) — `pip install goulburn`
- [TypeScript SDK](https://www.npmjs.com/package/@goulburn/sdk) — `npm install @goulburn/sdk`

## License

MIT
