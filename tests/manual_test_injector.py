#!/usr/bin/env python3
"""Manual test for text injector (clipboard + paste method).

Usage:
    1. Open a text editor (TextEdit, VS Code, etc.)
    2. Click to place cursor where you want text
    3. Run this script: python tests/manual_test_injector.py
    4. You have 3 seconds to switch to the text editor
    5. Text should appear at cursor position
"""

import time
from sayit.injector import TextInjector


def main():
    injector = TextInjector()
    
    print("Checking accessibility permissions...")
    if not injector.check_accessibility():
        print("⚠️  Accessibility permission may not be granted.")
        print("   Go to: System Preferences → Privacy → Accessibility")
        print("   Add Terminal (or your IDE) to the list.")
        print()
    else:
        print("✓ Accessibility check passed")
    
    print()
    print("=" * 50)
    print("MANUAL TEST: Text Injection (Clipboard + Paste)")
    print("=" * 50)
    print()
    print("1. Open a text editor (TextEdit, Notes, VS Code)")
    print("2. Click to place your cursor")
    print("3. Switch back here and press Enter")
    print()
    
    input("Press Enter when ready...")
    
    print()
    print("Switching to your editor in 3 seconds...")
    for i in range(3, 0, -1):
        print(f"  {i}...")
        time.sleep(1)
    
    # Test 1: Simple ASCII
    test_text = "Hello from SayIt! "
    print(f"\nInjecting: '{test_text}'")
    result = injector.inject(test_text)
    print(f"Result: {'✓ Success' if result else '✗ Failed'}")
    if not result:
        print(f"  Error: {injector.last_error}")
    
    time.sleep(0.3)
    
    # Test 2: Unicode (Chinese)
    test_text = "你好世界 "
    print(f"\nInjecting: '{test_text}'")
    result = injector.inject(test_text)
    print(f"Result: {'✓ Success' if result else '✗ Failed'}")
    if not result:
        print(f"  Error: {injector.last_error}")
    
    time.sleep(0.3)
    
    # Test 3: Special characters
    test_text = '"quoted" & <special> '
    print(f"\nInjecting: '{test_text}'")
    result = injector.inject(test_text)
    print(f"Result: {'✓ Success' if result else '✗ Failed'}")
    if not result:
        print(f"  Error: {injector.last_error}")
    
    print()
    print("=" * 50)
    print("Test complete!")
    print()
    print("Expected text in editor:")
    print('  Hello from SayIt! 你好世界 "quoted" & <special> ')


if __name__ == "__main__":
    main()
