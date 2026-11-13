"""Offline tests for safe credential diagnostics."""
from pathlib import Path

from receptionist.preflight import check_environment


def test_missing_file(tmp_path):
    assert check_environment(tmp_path / ".env", {}) == [".env file missing"]


def test_present_values_do_not_mean_authenticated(tmp_path):
    env = tmp_path / ".env"
    env.write_text(
        "LIVEKIT_URL=wss://example.livekit.cloud\n"
        "LIVEKIT_API_KEY=key-id\n"
        "LIVEKIT_API_SECRET=secret-value\n"
        "OPENAI_API_KEY=sk-proj-not-a-real-key\n",
        encoding="utf-8",
    )
    assert check_environment(env, {}) == []


def test_detects_stale_shell_override_without_leaking_secret(tmp_path):
    env = tmp_path / ".env"
    env.write_text(
        "LIVEKIT_URL=wss://example.livekit.cloud\n"
        "LIVEKIT_API_KEY=key-id\n"
        "LIVEKIT_API_SECRET=secret-value\n"
        "OPENAI_API_KEY=sk-proj-file-value\n",
        encoding="utf-8",
    )
    errors = check_environment(env, {"OPENAI_API_KEY": "sk-proj-old-shell-value"})
    assert any("overrides .env" in error for error in errors)
    assert "old-shell-value" not in str(errors)
    assert "file-value" not in str(errors)


def test_detects_placeholder_and_url(tmp_path):
    env = tmp_path / ".env"
    env.write_text(
        "LIVEKIT_URL=https://wrong\n"
        "LIVEKIT_API_KEY=your-key\n"
        "LIVEKIT_API_SECRET=secret\n"
        "OPENAI_API_KEY=placeholder\n",
        encoding="utf-8",
    )
    errors = check_environment(env, {})
    assert any("LIVEKIT_URL: expected" in e for e in errors)
    assert any("placeholder" in e for e in errors)


def test_detects_env_local_precedence(tmp_path):
    env = tmp_path / ".env"
    env.write_text(
        "LIVEKIT_URL=wss://example.livekit.cloud\n"
        "LIVEKIT_API_KEY=key-id\n"
        "LIVEKIT_API_SECRET=secret-value\n"
        "OPENAI_API_KEY=sk-proj-current\n",
        encoding="utf-8",
    )
    (tmp_path / ".env.local").write_text(
        "OPENAI_API_KEY=sk-proj-stale\n", encoding="utf-8"
    )
    errors = check_environment(env, {})
    assert any(".env.local takes precedence" in e for e in errors)
    assert "sk-proj-stale" not in str(errors)
