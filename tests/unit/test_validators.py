from __future__ import annotations

from core.validators.consistency import is_consistent
from core.validators.relevance import is_relevant


def test_is_relevant_matches_topic() -> None:
    assert is_relevant("cats", "All about cats and kittens.")


def test_is_consistent_basic() -> None:
    assert is_consistent("anchor", "child")
