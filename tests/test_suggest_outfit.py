"""
Tests for suggest_outfit() in tools.py.

Groq is mocked so tests run without a live API key and return deterministic output.
"""

from unittest.mock import MagicMock, patch

import pytest

from tools import suggest_outfit

# ── Fixtures ──────────────────────────────────────────────────────────────────

GRUNGE_ITEM = {
    "title": "Vintage Nirvana Graphic Tee",
    "category": "tops",
    "colors": ["black", "white"],
    "style_tags": ["vintage", "grunge", "graphic"],
    "condition": "Good",
    "description": "Faded 90s band tee with distressed hem.",
}

FORMAL_ITEM = {
    "title": "Wool Herringbone Blazer",
    "category": "outerwear",
    "colors": ["charcoal", "grey"],
    "style_tags": ["formal", "office", "tailored"],
    "condition": "Excellent",
    "description": "Structured single-breasted blazer, slim fit.",
}

STREETWEAR_WARDROBE = {
    "items": [
        {
            "id": "w_001",
            "name": "Baggy straight-leg jeans, dark wash",
            "category": "bottoms",
            "colors": ["dark blue", "indigo"],
            "style_tags": ["denim", "streetwear", "baggy"],
            "notes": "High-waisted, sits above the hip",
        },
        {
            "id": "w_008",
            "name": "Black combat boots",
            "category": "shoes",
            "colors": ["black"],
            "style_tags": ["boots", "grunge", "classic"],
            "notes": "Lace-up, mid-ankle height",
        },
    ]
}

EMPTY_WARDROBE = {"items": []}


def _mock_groq(reply: str):
    """Return a patch context that makes Groq return `reply`."""
    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value.choices[
        0
    ].message.content = reply
    return patch("tools.Groq", return_value=mock_client)


# ── Tests ─────────────────────────────────────────────────────────────────────


def test_wardrobe_with_matching_style_references_specific_pieces():
    """With a style-compatible wardrobe, the response mentions wardrobe piece names."""
    expected = (
        "Pair the Nirvana tee with your Baggy straight-leg jeans and Black combat boots "
        "for a classic 90s grunge look."
    )
    with _mock_groq(expected):
        result = suggest_outfit(GRUNGE_ITEM, STREETWEAR_WARDROBE)

    assert isinstance(result, str)
    assert len(result) > 0
    # LLM was given wardrobe item names — response should echo at least one back
    wardrobe_names = [item["name"] for item in STREETWEAR_WARDROBE["items"]]
    assert any(name in result for name in wardrobe_names)


def test_wardrobe_with_mismatched_style_still_returns_suggestion():
    """Even when the new item clashes with the wardrobe vibe, a non-empty suggestion is returned."""
    expected = (
        "The blazer is more formal than your current wardrobe, but try it over your "
        "Baggy straight-leg jeans for a high-low contrast look."
    )
    with _mock_groq(expected):
        result = suggest_outfit(FORMAL_ITEM, STREETWEAR_WARDROBE)

    assert isinstance(result, str)
    assert len(result) > 0


def test_empty_wardrobe_returns_general_styling_advice():
    """With an empty wardrobe, suggest_outfit() returns general advice without crashing."""
    expected = (
        "This graphic tee works great as a base layer — try pairing it with wide-leg "
        "trousers or baggy denim and chunky sneakers for a relaxed 90s vibe."
    )
    with _mock_groq(expected):
        result = suggest_outfit(GRUNGE_ITEM, EMPTY_WARDROBE)

    assert isinstance(result, str)
    assert len(result) > 0
