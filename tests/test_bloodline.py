"""Offline Bloodline configuration and prompt acceptance checks."""
from pathlib import Path

from receptionist.config import load_config
from receptionist.prompts import build_system_prompt

PATH = Path("config/businesses/bloodline-hauling.yaml")


def test_bloodline_config_loads():
    config = load_config(PATH)
    assert config.business.name == "Bloodline Hauling Co."
    assert config.business.timezone == "America/Denver"
    assert config.agent.mode == "receptionist"
    assert config.voice.auth.type == "api_key"
    assert config.routing == []
    assert config.calendar is None
    assert config.recording is None


def test_bloodline_hours():
    config = load_config(PATH)
    for day in ("monday", "tuesday", "wednesday", "thursday", "friday"):
        hours = getattr(config.hours, day)
        assert hours.open == "09:00"
        assert hours.close == "18:00"
    assert config.hours.saturday is None
    assert config.hours.sunday is None


def test_bloodline_conversation_guardrails():
    config = load_config(PATH)
    prompt = build_system_prompt(config).lower()
    assert "preferred pickup date and time" in prompt
    assert "sms follow-up" in prompt
    assert "never claim an appointment was booked" in prompt
    assert "business hours" in prompt
    assert "09:00 - 18:00" in prompt
    assert "saturday: closed" in prompt
    assert "no routing configured" in prompt
