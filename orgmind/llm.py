import os

from anthropic import Anthropic

_client: Anthropic | None = None


def complete(system: str, prompt: str, max_tokens: int = 1500) -> str:
    global _client
    _client = _client or Anthropic()
    msg = _client.messages.create(
        model=os.getenv("ORGMIND_MODEL", "claude-sonnet-5-5"),
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": prompt}],
    )
    return "".join(b.text for b in msg.content if b.type == "text")
