# Phantom Shell 👻

> **Hacktoberfest 2026 · Week 4 DEV Challenge — *Ghost in the Machine***  
> A haunted terminal possessed by a **local open-weight model**.

Your shell runs the command. The **Phantom** whispers back — foreshadowing danger, celebrating cleverness, or just being eerie. No cloud API. Weights stay on your machine.

```
$ phantom run -- rm -rf /tmp/old-cache
👻 phantom [ollama/llama3.2]:
   Deleting… I keep a shadow of what was. The void is never empty.
```

## Theme interpretation

**Ghost in the Machine** is not a metaphor for “AI in the cloud.”  
Here the ghost *literally* lives in your machine: an open-weight model served by [Ollama](https://ollama.com) (or a documented llama.cpp path). Possession is a thin CLI wrap — every command gets haunted commentary, and you can chat with the phantom directly.

Open innovation matters because:

- **Privacy** — prompts and command context never leave the host
- **Offline** — demos and daily use work without an API key
- **Remixable** — MIT license, stdlib-first Python, swap models freely

## Open-source AI used

| Layer | Choice |
|-------|--------|
| Runtime | [Ollama](https://ollama.com) (`/api/chat`) |
| Default model | `llama3.2` (override with `--model` / `$PHANTOM_MODEL`) |
| Fallbacks | any Ollama tag: `phi3`, `qwen2.5`, `gemma2`, `mistral`, … |
| Offline demo | built-in **mock ghost** when Ollama is down (`--mock` / `$PHANTOM_MOCK=1`) |
| Optional | [llama.cpp](https://github.com/ggerganov/llama.cpp) server — point `--host` at its OpenAI-compatible proxy *or* use Ollama’s llama.cpp backend |

Core idea: **open weights + local inference = the ghost is yours.**

## Requirements

- Python **3.10+** (3.13 tested)
- Optional: [Ollama](https://ollama.com) + a small open model
- Zero pip dependencies for core (stdlib only)

## Quick start

```bash
git clone https://github.com/pr7426/ghost-in-the-machine.git
cd ghost-in-the-machine

# works immediately (mock mode if Ollama is offline)
python3 -m phantom_shell status
python3 -m phantom_shell demo
python3 -m phantom_shell run -- echo "boo"
python3 -m phantom_shell chat "Who are you?"
python3 -m phantom_shell possess
```

Install as a console script (optional):

```bash
pip install -e .
phantom status
phantom possess
```

### Wake the real ghost (Ollama)

```bash
# install from https://ollama.com , then:
ollama pull llama3.2
python3 -m phantom_shell status
python3 -m phantom_shell run --model llama3.2 -- git status
python3 -m phantom_shell possess --model llama3.2
```

Environment knobs:

| Variable | Meaning |
|----------|---------|
| `OLLAMA_HOST` | default `http://127.0.0.1:11434` |
| `PHANTOM_MODEL` | default `llama3.2` |
| `PHANTOM_MOCK` | `1` forces offline mock ghost |

### llama.cpp path (optional)

1. Run a local server (Ollama already embeds llama.cpp; or use `llama-server`).
2. If you expose an Ollama-compatible `/api/chat`, set `--host`.
3. Or keep using Ollama and select a GGUF-backed model tag — same CLI.

## Demo / recording

```bash
./scripts/demo.sh
# see scripts/record_demo.md for asciinema + GIF tips
```

A captured text session lives in [`demo/sample_session.txt`](demo/sample_session.txt).

## CLI map

| Command | What it does |
|---------|----------------|
| `phantom status` | Banner + Ollama / model health |
| `phantom run -- <cmd>` | Run a shell command, print haunted commentary |
| `phantom chat <msg>` | Talk to the phantom |
| `phantom possess` | Interactive haunted REPL (`.chat`, `.status`, `.quit`) |
| `phantom demo` | Scripted judge-friendly walkthrough (`--live` for real model) |

## Project layout

```
phantom_shell/          # Python package (CLI + Ollama client + mock)
scripts/demo.sh         # one-shot mock demo
scripts/record_demo.md  # asciinema / GIF notes
demo/sample_session.txt # checked-in transcript
DEV_SUBMISSION.md       # draft DEV.to Week 4 post
```

## Why this for Week 4

- **Started in the Oct 28–31 2026 window** — new project, not a recycled Week 2 repo  
- **Open-source AI at the core** — Ollama + open weights, not a closed API  
- **Runnable demo** — `phantom demo` works with zero GPU and zero network  
- **English README + MIT** — ready for the DEV write-up  

## License

[MIT](LICENSE) © 2026 Ri Piao ([@pr742674](https://x.com/pr742674))

## Credits

Built for [Hacktoberfest 2026](https://hacktoberfest.com/) · DEV Challenge Week 4 · *Ghost in the Machine*.
