"""Thin Ollama HTTP client (stdlib only) + automatic mock fallback."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Generator, Optional

from phantom_shell import mock as mock_ghost
from phantom_shell.prompts import CHAT_HINT, COMMENT_TEMPLATE, SYSTEM_GHOST

DEFAULT_HOST = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434")
DEFAULT_MODEL = os.environ.get("PHANTOM_MODEL", "llama3.2")


@dataclass
class GhostReply:
    text: str
    source: str  # "ollama" | "mock"
    model: str


class OllamaClient:
    def __init__(
        self,
        host: str = DEFAULT_HOST,
        model: str = DEFAULT_MODEL,
        force_mock: bool = False,
        timeout: float = 120.0,
    ):
        self.host = host.rstrip("/")
        self.model = model
        self.force_mock = force_mock or os.environ.get("PHANTOM_MOCK", "").lower() in (
            "1",
            "true",
            "yes",
        )
        self.timeout = timeout

    def available(self) -> bool:
        if self.force_mock:
            return False
        try:
            with urllib.request.urlopen(f"{self.host}/api/tags", timeout=2) as resp:
                return resp.status == 200
        except Exception:
            return False

    def list_models(self) -> list[str]:
        if not self.available():
            return []
        try:
            with urllib.request.urlopen(f"{self.host}/api/tags", timeout=5) as resp:
                data = json.loads(resp.read().decode())
            return [m.get("name", "") for m in data.get("models", [])]
        except Exception:
            return []

    def _chat(self, user_content: str, stream: bool = False) -> str:
        payload = {
            "model": self.model,
            "stream": stream,
            "messages": [
                {"role": "system", "content": SYSTEM_GHOST},
                {"role": "user", "content": user_content},
            ],
        }
        req = urllib.request.Request(
            f"{self.host}/api/chat",
            data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=self.timeout) as resp:
            if stream:
                chunks: list[str] = []
                for line in resp:
                    if not line.strip():
                        continue
                    obj = json.loads(line.decode())
                    part = obj.get("message", {}).get("content", "")
                    if part:
                        chunks.append(part)
                    if obj.get("done"):
                        break
                return "".join(chunks)
            data = json.loads(resp.read().decode())
            return data.get("message", {}).get("content", "").strip()

    def _chat_stream(self, user_content: str) -> Generator[str, None, None]:
        payload = {
            "model": self.model,
            "stream": True,
            "messages": [
                {"role": "system", "content": SYSTEM_GHOST},
                {"role": "user", "content": user_content},
            ],
        }
        req = urllib.request.Request(
            f"{self.host}/api/chat",
            data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=self.timeout) as resp:
            for line in resp:
                if not line.strip():
                    continue
                obj = json.loads(line.decode())
                part = obj.get("message", {}).get("content", "")
                if part:
                    yield part
                if obj.get("done"):
                    break

    def comment(
        self,
        command: str,
        exit_code: int,
        stdout: str = "",
        stderr: str = "",
    ) -> GhostReply:
        stdout_t = (stdout or "")[:800] or "(empty)"
        stderr_t = (stderr or "")[:400] or "(empty)"
        prompt = COMMENT_TEMPLATE.format(
            command=command,
            exit_code=exit_code,
            stdout=stdout_t,
            stderr=stderr_t,
        )
        if self.available():
            try:
                text = self._chat(prompt)
                return GhostReply(text=text.strip(), source="ollama", model=self.model)
            except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError):
                pass
        text = mock_ghost.mock_comment(command, exit_code, stdout, stderr)
        return GhostReply(text=text, source="mock", model="mock-phantom")

    def chat(self, message: str) -> GhostReply:
        prompt = CHAT_HINT.format(message=message)
        if self.available():
            try:
                text = self._chat(prompt)
                return GhostReply(text=text.strip(), source="ollama", model=self.model)
            except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError):
                pass
        text = mock_ghost.mock_chat(message)
        return GhostReply(text=text, source="mock", model="mock-phantom")

    def chat_stream(self, message: str) -> tuple[str, Generator[str, None, None]]:
        """Return (source_label, token generator)."""
        prompt = CHAT_HINT.format(message=message)
        if self.available():
            try:
                # Probe with a quick availability; stream for real
                gen = self._chat_stream(prompt)
                return "ollama", gen
            except Exception:
                pass
        text = mock_ghost.mock_chat(message)
        return "mock", mock_ghost.mock_stream(text)


def truncate_for_display(s: str, limit: int = 2000) -> str:
    if len(s) <= limit:
        return s
    return s[:limit] + f"\n… [{len(s) - limit} bytes truncated by Phantom]"
