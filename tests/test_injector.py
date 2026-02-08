"""Tests for text injector."""

import pytest
from sayit.injector import TextInjector


class TestTextInjector:
    """Unit tests for TextInjector."""

    def test_empty_text_returns_true(self):
        """Empty text injection returns True without action."""
        injector = TextInjector()
        assert injector.inject("") is True

    def test_last_error_initially_none(self):
        """last_error is None before any errors occur."""
        injector = TextInjector()
        assert injector.last_error is None


@pytest.mark.hardware
class TestTextInjectorHardware:
    """Hardware tests requiring accessibility permissions.
    
    Run with: pytest -m hardware
    These tests actually inject text, so run with caution.
    """

    def test_check_accessibility(self):
        """Check if accessibility permissions are granted."""
        injector = TextInjector()
        result = injector.check_accessibility()
        print(f"Accessibility check: {result}")

    def test_inject_ascii(self):
        """Inject ASCII text via clipboard+paste."""
        injector = TextInjector()
        # WARNING: This will paste text wherever cursor is!
        # result = injector.inject("Hello")
        print("Skipped: would paste 'Hello' at cursor")

    def test_inject_unicode(self):
        """Inject Unicode text via clipboard+paste."""
        injector = TextInjector()
        # WARNING: This will paste text wherever cursor is!
        # result = injector.inject("你好世界")
        print("Skipped: would paste '你好世界' at cursor")
