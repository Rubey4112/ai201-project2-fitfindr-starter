"""
Tests for search_listings() in tools.py.
"""

import pytest
from tools import search_listings


def test_keyword_match_returns_relevant_results():
    """Results contain the queried keyword somewhere in their fields."""
    results = search_listings("vintage denim")
    assert len(results) > 0
    for item in results:
        searchable = " ".join([
            item["title"],
            item["description"],
            item["category"],
            " ".join(item["style_tags"]),
            " ".join(item["colors"]),
        ]).lower()
        assert "vintage" in searchable or "denim" in searchable


def test_price_filter_excludes_expensive_items():
    """No returned item exceeds max_price."""
    max_price = 30.0
    results = search_listings("graphic tee", max_price=max_price)
    assert len(results) > 0
    for item in results:
        assert item["price"] <= max_price


def test_no_match_returns_empty_list():
    """A nonsense description with a very low price ceiling returns nothing."""
    results = search_listings("xyzzy nonsense garment", max_price=0.01)
    assert results == []


def test_search_returns_results():
    results = search_listings("vintage graphic tee", size=None, max_price=50)
    assert isinstance(results, list)
    assert len(results) > 0

def test_search_empty_results():
    results = search_listings("designer ballgown", size="XXS", max_price=5)
    assert results == []   # empty list, no exception

def test_search_price_filter():
    results = search_listings("jacket", size=None, max_price=10)
    assert all(item["price"] <= 10 for item in results)
