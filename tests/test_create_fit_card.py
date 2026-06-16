"""
Tests for create_fit_card() in tools.py.

Groq is mocked so tests run without a live API key and return deterministic output.
"""

from unittest.mock import MagicMock, patch

import pytest

from tools import create_fit_card

# ── Fixtures ──────────────────────────────────────────────────────────────────

DENIM_ITEM = {
    "title": "Levi's 501 Straight-Leg Jeans",
    "price": 28.00,
    "platform": "Depop",
    "colors": ["light blue", "indigo"],
    "style_tags": ["denim", "vintage", "streetwear"],
}

COMPLETE_OUTFIT = (
    "Pair the Levi's 501s with a white cropped tank and chunky white sneakers "
    "for a clean, effortless 90s look."
)

WHITESPACE_OUTFIT = "   \t\n  "


def _mock_groq(reply: str):
    """Return a patch context that makes Groq return `reply`."""
    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value.choices[
        0
    ].message.content = reply
    return patch("tools.Groq", return_value=mock_client)


# ── Tests ─────────────────────────────────────────────────────────────────────


def test_complete_outfit_returns_caption_with_item_details():
    """A full outfit + item dict produces a non-empty caption mentioning the item name, price, and platform."""
    expected = (
        "thrifted these Levi's 501 Straight-Leg Jeans off Depop for $28.00 and they are "
        "everything. cropped tank, chunky sneakers — pure 90s and I'm not sorry."
    )
    with _mock_groq(expected):
        result = create_fit_card(COMPLETE_OUTFIT, DENIM_ITEM)

    assert isinstance(result, str)
    assert len(result) > 0
    assert "Levi's 501 Straight-Leg Jeans" in result
    assert "Depop" in result
    assert "28" in result  # price appears somewhere in the caption


def test_partial_outfit_still_returns_caption():
    """A brief or incomplete outfit description still produces a caption without crashing."""
    sparse_outfit = "Looks good with jeans."
    expected = "grabbed this off Depop for $28.00 and honestly the minimal styling sold it."
    with _mock_groq(expected):
        result = create_fit_card(sparse_outfit, DENIM_ITEM)

    assert isinstance(result, str)
    assert len(result) > 0


def test_empty_outfit_returns_error_string_not_exception():
    """An empty or whitespace-only outfit string returns a descriptive error, not an exception."""
    for bad_input in ("", WHITESPACE_OUTFIT):
        result = create_fit_card(bad_input, DENIM_ITEM)
        assert isinstance(result, str)
        assert len(result) > 0
        assert "error" in result.lower() or "suggest_outfit" in result.lower()
