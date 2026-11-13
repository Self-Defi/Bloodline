"""Safe, read-only Bloodline voice-agent readiness checks.

Run: python -m receptionist.preflight
     python -m receptionist.preflight --verify-openai
Never prints credential contents or provider error bodies.
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path

from dotenv import dotenv_values


REQUIRED = ("LIVEKIT_URL", "LIVEKIT_API_KEY", "LIVEKIT_API_SECRET", "OPENAI_API_KEY")


def check_environment(path: Path = Path(".env"), environ=None) -> list[str]:
    """Return human-readable failures without exposing credentials."""
    errors: list[str] = []
    if not path.is_file():
        return [".env file missing"]
    values = dotenv_values(path)
    environ = os.environ if environ is None else environ
    for name in REQUIRED:
        value = values.get(name)
        if not value or not value.strip():
            errors.append(f"{name}: missing from .env")
        elif value != value.strip():
            errors.append(f"{name}: leading or trailing whitespace")
        elif value.lower().startswith(("your-", "your_", "placeholder", "replace_me")):
            errors.append(f"{name}: placeholder value")
        if environ.get(name) and value and environ[name] != value:
            errors.append(f"{name}: process environment overrides .env with a different value")
    url = values.get("LIVEKIT_URL") or ""
    if url and not (url.startswith("wss://") or url.startswith("ws://")):
        errors.append("LIVEKIT_URL: expected ws:// or wss://")
    return errors


def verify_openai(path: Path = Path(".env")) -> str:
    """Check provider authentication, without displaying a key or response body."""
    from openai import OpenAI, AuthenticationError, PermissionDeniedError, RateLimitError, APIConnectionError, APIStatusError

    key = dotenv_values(path).get("OPENAI_API_KEY")
    if not key:
        return "FAIL: OPENAI_API_KEY missing"
    try:
        OpenAI(api_key=key, timeout=12.0, max_retries=0).models.list()
    except AuthenticationError:
        return "FAIL: OpenAI rejected the key (HTTP 401). Check project/key validity."
    except PermissionDeniedError:
        return "FAIL: OpenAI denied access (HTTP 403). Check project permissions."
    except RateLimitError:
        return "FAIL: OpenAI rate limit or quota restriction (HTTP 429)."
    except APIConnectionError:
        return "FAIL: Could not reach OpenAI. Check network/TLS."
    except APIStatusError as exc:
        return f"FAIL: OpenAI returned HTTP {exc.status_code}."
    return "PASS: OpenAI accepted the API key for models.list (Realtime access not yet tested)."


def main() -> int:
    parser = argparse.ArgumentParser(description="Credential-safe receptionist preflight")
    parser.add_argument("--verify-openai", action="store_true", help="Make a read-only API authentication request")
    args = parser.parse_args()
    failures = check_environment()
    if failures:
        for failure in failures:
            print("FAIL:", failure)
        print("No credentials were displayed.")
        return 1
    print("PASS: .env values present; no conflicting process overrides detected.")
    if args.verify_openai:
        outcome = verify_openai()
        print(outcome)
        return 0 if outcome.startswith("PASS:") else 1
    print("NOTE: Presence is not authentication. Use --verify-openai to check with the provider.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
