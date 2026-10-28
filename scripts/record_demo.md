# Recording a demo

## Quick (no install)

```bash
cd ghost-in-the-machine
./scripts/demo.sh
```

## asciinema (recommended for DEV.to)

```bash
# install asciinema: https://asciinema.org/docs/installation
cd ghost-in-the-machine
asciinema rec demo/phantom-shell.cast --command './scripts/demo.sh'
# optional GIF via agg: https://github.com/asciinema/agg
agg demo/phantom-shell.cast demo/phantom-shell.gif
```

## With a live local model

```bash
ollama pull llama3.2   # or phi3, qwen2.5, gemma2, …
python3 -m phantom_shell demo --live --model llama3.2
# or interactive:
python3 -m phantom_shell possess --model llama3.2
```

## One-liners for screenshots

```bash
python3 -m phantom_shell status
python3 -m phantom_shell run -- echo "boo"
python3 -m phantom_shell chat "Why does open-source AI matter?"
```
