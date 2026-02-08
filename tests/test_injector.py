"""Tests for text injector."""

import pytest
from sayit.injector import TextInjector


class TestTextInjector:
    """Unit tests for TextInjector."""

    def test_escape_backslash(self):
        """Backslashes are escaped for AppleScript."""
        injector = TextInjector()
        result = injector._escape_for_applescript("path\\to\\file")
        assert result == "path\\\\to\\\\file"

    def test_escape_quotes(self):
        """Double quotes are escaped for AppleScript."""
        injector = TextInjector()
        result = injector._escape_for_applescript('say "hello"')
        assert result == 'say \\"hello\\"'

    def test_escape_mixed(self):
        """Mixed special characters are escaped correctly."""
        injector = TextInjector()
        result = injector._escape_for_applescript('path\\to\\"file"')
        assert result == 'path\\\\to\\\\\\"file\\"'

    def test_escape_unicode(self):
        """Unicode characters pass through unchanged."""
        injector = TextInjector()
        result = injector._escape_for_applescript("你好世界")
        assert result == "你好世界"

    def test_empty_text_returns_true(self):
        """Empty text injection returns True without action."""
        injector = TextInjector()
        assert injector.inject("") is True


@pytest.mark.hardware
class TestTextInjectorHardware:
    """Hardware tests requiring accessibility permissions.
    
    Run with: pytest -m hardware
    These tests actually inject text, so run with caution.
    """

    def test_check_accessibility(self):
        """Check if accessibility permissions are granted."""
        injector = TextInjector()
        # This will return True if permissions granted, False otherwise
        result = injector.check_accessibility()
        print(f"Accessibility check: {result}")
        # Don't assert - just report status

    def test_inject_simple_text(self):
        """Inject simple ASCII text."""
        injector = TextInjector()
        # WARNING: This will type text wherever cursor is!
        # result = injector.inject("test")
        print("Skipped: would type 'test' at cursor")

    def test_inject_unicode(self):
        """Inject Unicode text."""
        injector = TextInjector()
        # WARNING: This will type text wherever cursor is!
        # result = injector.inject("你好")
        print("Skipped: would type '你好' at cursor")
