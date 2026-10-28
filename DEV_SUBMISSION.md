---
title: "Phantom Shell — a haunted terminal possessed by a local open-weight model"
published: false
tags: devchallenge, hf26challenge, hacktoberfest, opensource, ai
# Week 4 — Ghost in the Machine
canonical_url:
cover_image:
---

# Phantom Shell 👻 — Ghost in the Machine (Hacktoberfest 2026 Week 4)

**Challenge:** `#devchallenge` `#hf26challenge` — Week 4 *Ghost in the Machine*  
**Author:** Ri Piao · X [@pr742674](https://x.com/pr742674) · email on GitHub profile

## What I built

**Phantom Shell** is a CLI that lets an open-weight model *possess* your terminal.

You run a normal shell command. The phantom — a local model via [Ollama](https://ollama.com) — whispers a short, eerie commentary about what you just did. You can also chat with it, or drop into `possess` mode: an interactive haunted REPL.

If Ollama is not installed, a built-in **mock ghost** still demos the full UX so judges (and you) can try it offline in seconds.

Theme take: the “ghost” should live *in the machine* — open weights, local inference, no cloud API key. Privacy is the haunting.

## Demo

```bash
git clone https://github.com/pr7426/ghost-in-the-machine.git
cd ghost-in-the-machine
python3 -m phantom_shell demo
# or:
./scripts/demo.sh
```

Interactive:

```bash
python3 -m phantom_shell possess
# phantom> echo boo
# phantom> .chat Who are you?
# phantom> .quit
```

With a real local model:

```bash
ollama pull llama3.2
python3 -m phantom_shell possess --model llama3.2
```

<!-- Optional: paste asciinema / GIF after you record (see scripts/record_demo.md)
[![asciicast](https://asciinema.org/a/XXXX.svg)](https://asciinema.org/a/XXXX)
-->

Sample transcript (checked into the repo): `demo/sample_session.txt`

## Repository

🔗 **Repo:** https://github.com/pr7426/ghost-in-the-machine  
*(replace `pr7426` with your GitHub username after push)*

License: **MIT** · Language: Python 3.10+ · Deps: **stdlib only** for core

## Open-source AI used

| Piece | Detail |
|-------|--------|
| Serving | Ollama (`/api/chat`) |
| Model | `llama3.2` by default (any Ollama open model works: `phi3`, `qwen2.5`, `gemma2`, …) |
| Offline | Mock ghost when Ollama is down |
| Optional path | llama.cpp / GGUF via Ollama or a local server (`--host`) |

No closed SaaS LLM is required for the core experience.

## Why open innovation matters (here)

- **Offline & private** — command context and chat stay on-device; great for a personal shell.
- **Swappable weights** — one flag changes the soul of the ghost; community models welcome.
- **Hackable** — tiny stdlib client, MIT, easy to fork into prompts, tools, or a full agentic shell.
- **Inclusive demos** — mock mode means anyone can run the challenge submission without a GPU.

Open weights turn “AI feature” into something you can *own*, inspect, and remix — which is the point of a Ghost that lives in *your* machine.

## Partner / bonus categories (optional)

If submitting under partner tracks later, note:

- Local-first / privacy tooling
- Developer experience CLI
- Open-model application (not training)

---

Thanks Hacktoberfest + DEV for Week 4 — may your shells stay haunted. 🎃
