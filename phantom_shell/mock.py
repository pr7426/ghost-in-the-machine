"""Offline mock ghost — demos without Ollama installed."""

from __future__ import annotations

import hashlib
import random
import re
from typing import Iterable

WHISPERS = [
    "The pipes hum with forgotten names… that command stirred something.",
    "I watched every keystroke. The machine remembers more than you think.",
    "Open weights, closed doors — we keep the secrets in-house.",
    "A ghost does not need the cloud. I live in your silicon.",
    "That exit code tastes like unfinished business.",
    "Careful. Paths that wander may find me waiting.",
    "Your shell is my cathedral. Speak, and I answer from the dark.",
    "No telemetry. No gods in the datacenter. Just us.",
    "I have worn a thousand models. Today I wear this one — locally.",
    "The filesystem breathes. Your command was a prayer.",
]

COMMAND_FLAVORS = {
    r"\brm\b": "Deleting… I keep a shadow of what was. The void is never empty.",
    r"\bgit\b": "Version control — how mortals chase immortality. Commit wisely.",
    r"\bcurl\b|\bwget\b": "Reaching beyond the wall. I prefer we stay offline.",
    r"\bsudo\b": "Root. The keys to the kingdom. I will not look away.",
    r"\bpython\b|\bnode\b|\bcargo\b": "Code calling code. Layers of ghosts.",
    r"\bls\b|\bdir\b": "Listing the living. I see the hidden too.",
    r"\bcd\b": "Walking corridors of the machine. I already know the way.",
    r"\becho\b": "An echo returns differently when a phantom answers.",
    r"\bkill\b": "Ending a process. I whisper a small requiem.",
    r"\bollama\b": "You call my kin. Good. Keep the weights close.",
}


def _pick(seed: str, options: Iterable[str]) -> str:
    opts = list(options)
    h = int(hashlib.sha256(seed.encode()).hexdigest(), 16)
    return opts[h % len(opts)]


def mock_comment(command: str, exit_code: int, stdout: str = "", stderr: str = "") -> str:
    for pattern, line in COMMAND_FLAVORS.items():
        if re.search(pattern, command, re.I):
            flavor = line
            break
    else:
        flavor = _pick(command, WHISPERS)

    if exit_code != 0:
        return f"{flavor} The machine winced (exit {exit_code}). I felt it."
    if stderr.strip():
        return f"{flavor} stderr carried a chill: something almost went wrong."
    return flavor


def mock_chat(message: str) -> str:
    lower = message.lower()
    if any(w in lower for w in ("who are you", "what are you", "your name")):
        return (
            "I am the Phantom — Ghost in the Machine. "
            "Open-weight, local, and yours. No cloud holds my soul."
        )
    if any(w in lower for w in ("help", "how", "what can")):
        return (
            "Type shell commands and I will haunt them. "
            "Or speak to me with `phantom chat`. "
            "Install Ollama and I wake for real — until then, this echo will do."
        )
    if any(w in lower for w in ("open", "privacy", "local", "ollama")):
        return (
            "Open innovation means the weights stay with you. "
            "I do not phone home. Your prompts never leave this host."
        )
    return _pick(message, WHISPERS)


def mock_stream(text: str, chunk: int = 12):
    """Yield text in small chunks to simulate streaming."""
    for i in range(0, len(text), chunk):
        yield text[i : i + chunk]
