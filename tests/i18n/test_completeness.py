"""Tests for English-only translation configuration."""

from __future__ import annotations

from ductor_bot.i18n import LANGUAGES, get_language, init


def test_only_english_language_is_registered() -> None:
    assert LANGUAGES == {"en": "English"}


def test_init_falls_back_to_english_for_removed_language() -> None:
    init("de")
    assert get_language() == "en"
