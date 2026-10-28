#!/usr/bin/env python3
"""Phantom Shell CLI — possess your terminal with a local open-weight ghost."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

from phantom_shell import __version__
from phantom_shell.ollama_client import DEFAULT_HOST, DEFAULT_MODEL, OllamaClient
from phantom_shell.prompts import BANNER

DIM = "\033[2m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"
BOLD = "\033[1m"


def _c(enabled: bool, code: str, text: str) -> str:
    if not enabled:
        return text
    return f"{code}{text}{RESET}"


def _want_color(args_color: str) -> bool:
    if args_color == "always":
        return True
    if args_color == "never":
        return False
    return sys.stdout.isatty() and os.environ.get("NO_COLOR") is None


def build_client(args) -> OllamaClient:
    return OllamaClient(
        host=getattr(args, "host", DEFAULT_HOST),
        model=getattr(args, "model", DEFAULT_MODEL),
        force_mock=getattr(args, "mock", False),
    )


def cmd_status(args) -> int:
    color = _want_color(args.color)
    client = build_client(args)
    print(_c(color, BOLD + MAGENTA, BANNER))
    print(f"  version : {__version__}")
    print(f"  host    : {client.host}")
    print(f"  model   : {client.model}")
    live = client.available()
    if live:
        models = client.list_models()
        print(_c(color, GREEN, "  ollama  : online"))
        print(f"  models  : {', '.join(models) or '(none pulled)'}")
        joined = " ".join(models)
        if client.model not in joined and not any(client.model in m for m in models):
            print(
                _c(
                    color,
                    YELLOW,
                    f"  tip     : pull with  ollama pull {client.model}",
                )
            )
    else:
        print(_c(color, YELLOW, "  ollama  : offline → using mock ghost"))
        print("  tip     : install https://ollama.com then: ollama pull llama3.2")
    return 0


def cmd_run(args) -> int:
    color = _want_color(args.color)
    client = build_client(args)
    command = args.command
    if isinstance(command, list):
        command = " ".join(command)
    command = command.strip()
    if not command:
        print("phantom run: need a command", file=sys.stderr)
        return 2

    print(_c(color, DIM, f"$ {command}"))
    try:
        proc = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            cwd=args.cwd or None,
        )
    except Exception as exc:
        print(_c(color, YELLOW, f"[phantom] could not run: {exc}"), file=sys.stderr)
        return 1

    if proc.stdout:
        sys.stdout.write(proc.stdout)
        if not proc.stdout.endswith("\n"):
            sys.stdout.write("\n")
    if proc.stderr:
        sys.stderr.write(proc.stderr)
        if not proc.stderr.endswith("\n"):
            sys.stderr.write("\n")

    reply = client.comment(command, proc.returncode, proc.stdout, proc.stderr)
    tag = "ollama" if reply.source == "ollama" else "mock"
    print()
    print(
        _c(color, MAGENTA, "👻 phantom")
        + _c(color, DIM, f" [{tag}/{reply.model}]")
        + ":"
    )
    print(_c(color, CYAN, f"   {reply.text}"))
    return proc.returncode


def cmd_chat(args) -> int:
    color = _want_color(args.color)
    client = build_client(args)
    message = args.message
    if isinstance(message, list):
        message = " ".join(message)
    message = (message or "").strip()
    if not message:
        print("phantom chat: need a message", file=sys.stderr)
        return 2

    source, stream = client.chat_stream(message)
    model = client.model if source == "ollama" else "mock-phantom"
    print(
        _c(color, MAGENTA, "👻 phantom")
        + _c(color, DIM, f" [{source}/{model}]")
        + ":"
    )
    sys.stdout.write("   ")
    try:
        for chunk in stream:
            sys.stdout.write(_c(color, CYAN, chunk) if color else chunk)
            sys.stdout.flush()
    except Exception as exc:
        reply = client.chat(message)
        print(_c(color, CYAN, reply.text))
        print(_c(color, DIM, f"(stream failed: {exc})"), file=sys.stderr)
        return 0
    print()
    return 0


def cmd_possess(args) -> int:
    color = _want_color(args.color)
    client = build_client(args)
    print(_c(color, BOLD + MAGENTA, BANNER))
    live = client.available()
    mode = f"ollama/{client.model}" if live else "mock ghost"
    print(
        _c(
            color,
            DIM,
            f"Possessed mode ({mode}). Type commands, or .chat <msg>, .status, .quit",
        )
    )
    print()

    while True:
        try:
            line = input(_c(color, GREEN, "phantom> ") if color else "phantom> ")
        except (EOFError, KeyboardInterrupt):
            print()
            print(_c(color, DIM, "The ghost returns to sleep."))
            return 0

        line = line.strip()
        if not line:
            continue
        if line in {".quit", ".exit", "exit", "quit"}:
            print(_c(color, DIM, "The ghost returns to sleep."))
            return 0
        if line == ".status":
            cmd_status(args)
            continue
        if line.startswith(".chat "):
            ns = argparse.Namespace(**vars(args))
            ns.message = line[6:]
            cmd_chat(ns)
            continue
        if line == ".chat":
            print("usage: .chat <message>")
            continue

        ns = argparse.Namespace(**vars(args))
        ns.command = line
        ns.cwd = None
        cmd_run(ns)


def cmd_demo(args) -> int:
    color = _want_color(args.color)
    if not args.live:
        args.mock = True
    print(_c(color, BOLD + MAGENTA, BANNER))
    print(_c(color, DIM, "— scripted demo (Week 4 Ghost in the Machine) —"))
    print()

    steps = [
        ("run", "echo 'Hello from the haunted shell'"),
        ("run", "pwd"),
        ("run", "git --version || true"),
        ("chat", "Who are you, and why do open weights matter?"),
        ("chat", "What happens if I rm -rf something important?"),
    ]
    for kind, payload in steps:
        print(_c(color, YELLOW, f"⟶ {kind}: {payload}"))
        ns = argparse.Namespace(**vars(args))
        if kind == "run":
            ns.command = payload
            ns.cwd = str(Path.cwd())
            cmd_run(ns)
        else:
            ns.message = payload
            cmd_chat(ns)
        print()
    print(_c(color, GREEN, "Demo complete. Try: phantom possess"))
    return 0


def _add_common(sp: argparse.ArgumentParser) -> None:
    sp.add_argument(
        "--host",
        default=DEFAULT_HOST,
        help=f"Ollama host (default: {DEFAULT_HOST} or $OLLAMA_HOST)",
    )
    sp.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Ollama model (default: {DEFAULT_MODEL} or $PHANTOM_MODEL)",
    )
    sp.add_argument(
        "--mock",
        action="store_true",
        help="Force offline mock ghost (also: PHANTOM_MOCK=1)",
    )
    sp.add_argument(
        "--color",
        choices=("auto", "always", "never"),
        default="auto",
        help="Color output",
    )


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="phantom",
        description=(
            "Phantom Shell — a haunted terminal possessed by a local open-weight model."
        ),
    )
    p.add_argument(
        "--version", action="version", version=f"phantom-shell {__version__}"
    )
    _add_common(p)

    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("status", help="Show ghost / Ollama status")
    _add_common(s)
    s.set_defaults(func=cmd_status)

    s = sub.add_parser("run", help="Run a shell command and hear the ghost")
    _add_common(s)
    s.add_argument("--cwd", default=None)
    s.add_argument("command", nargs=argparse.REMAINDER, help="Command to run")
    s.set_defaults(func=cmd_run)

    s = sub.add_parser("chat", help="Speak directly to the phantom")
    _add_common(s)
    s.add_argument("message", nargs="+", help="Message")
    s.set_defaults(func=cmd_chat)

    s = sub.add_parser("possess", help="Interactive haunted REPL")
    _add_common(s)
    s.set_defaults(func=cmd_possess)

    s = sub.add_parser("demo", help="Scripted demo for recordings / judges")
    _add_common(s)
    s.add_argument(
        "--live",
        action="store_true",
        help="Use real Ollama if available (default: force mock for reliable demos)",
    )
    s.set_defaults(func=cmd_demo)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if getattr(args, "command", None) is not None:
        cmd = list(args.command)
        if cmd and cmd[0] == "--":
            cmd = cmd[1:]
        args.command = " ".join(cmd)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
