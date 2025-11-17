"""
Test bind_two_way() in both common and uncommon usage patterns.

Tests cover:
1. Common case: bind_two_way() called AFTER page.add()
2. Uncommon case: bind_two_way() called BEFORE page.add()
"""

import flet as ft
import flet_asp as fa
import time


class MockPage:
    """Mock Flet Page for testing"""

    def __init__(self):
        self.added_controls = []
        self.update_count = 0

    def add(self, *controls):
        """Simulate page.add()"""
        self.added_controls.extend(controls)
        for control in controls:
            if hasattr(control, "ref") and control.ref is not None:
                control.ref.current = control
                # Simulate page assignment
                control.page = self

    def update(self):
        """Simulate page.update()"""
        self.update_count += 1


def test_bind_two_way_common_case():
    """
    Test bind_two_way() when called AFTER page.add() (common case).

    This is the recommended usage pattern and should work immediately
    without any threading overhead.
    """
    print("\n=== Test: Common Case (bind AFTER page.add) ===")

    page = MockPage()
    state = fa.get_state_manager(page)

    # Create atoms
    state.atom("email", "")
    state.atom("count", 0)

    # Create refs
    email_ref = ft.Ref[ft.TextField]()

    # Track listener calls
    listener_calls = []

    def on_email_change(value):
        listener_calls.append(value)

    state.listen("email", on_email_change)

    # COMMON CASE: Add to page FIRST
    page.add(ft.TextField(ref=email_ref, label="Email"))

    # THEN create binding
    state.bind_two_way("email", email_ref)

    # Verify control exists
    assert email_ref.current is not None, "Control should exist after page.add"

    # Verify on_change is set
    assert email_ref.current.on_change is not None, "on_change should be set"

    # Simulate user typing by calling on_change
    class FakeEvent:
        def __init__(self, data):
            self.data = data
            self.control = email_ref.current

    email_ref.current.value = "test@example.com"
    email_ref.current.on_change(FakeEvent("test@example.com"))

    # Verify atom was updated
    assert state.get("email") == "test@example.com", (
        f"Expected 'test@example.com', got '{state.get('email')}'"
    )

    # Verify listener was called
    assert "test@example.com" in listener_calls, (
        f"Listener should be called with 'test@example.com', got {listener_calls}"
    )

    print("✅ Common case test passed!")


def test_bind_two_way_uncommon_case():
    """
    Test bind_two_way() when called BEFORE page.add() (uncommon case).

    This is less common but should still work - the implementation
    uses polling to wait for control.current to be ready.
    """
    print("\n=== Test: Uncommon Case (bind BEFORE page.add) ===")

    page = MockPage()
    state = fa.get_state_manager(page)

    # Create atoms
    state.atom("email", "")

    # Create refs
    email_ref = ft.Ref[ft.TextField]()

    # Track listener calls
    listener_calls = []

    def on_email_change(value):
        listener_calls.append(value)

    state.listen("email", on_email_change)

    # UNCOMMON CASE: Create binding FIRST (control.current is None)
    state.bind_two_way("email", email_ref)

    # THEN add to page
    page.add(ft.TextField(ref=email_ref, label="Email"))

    # Wait for polling to complete (max 100ms)
    time.sleep(0.15)  # 150ms to be safe

    # Verify control exists
    assert email_ref.current is not None, "Control should exist after page.add"

    # Verify on_change was set by the polling mechanism
    assert email_ref.current.on_change is not None, (
        "on_change should be set even in uncommon case"
    )

    # Simulate user typing
    class FakeEvent:
        def __init__(self, data):
            self.data = data
            self.control = email_ref.current

    email_ref.current.value = "uncommon@test.com"
    email_ref.current.on_change(FakeEvent("uncommon@test.com"))

    # Verify atom was updated
    assert state.get("email") == "uncommon@test.com", (
        f"Expected 'uncommon@test.com', got '{state.get('email')}'"
    )

    # Verify listener was called
    assert "uncommon@test.com" in listener_calls, (
        f"Listener should be called, got {listener_calls}"
    )

    print("✅ Uncommon case test passed!")


def test_bind_two_way_preserves_existing_handler():
    """
    Test that bind_two_way() preserves any existing on_change handler.

    This ensures we don't break user-defined handlers.
    """
    print("\n=== Test: Preserve Existing Handler ===")

    page = MockPage()
    state = fa.get_state_manager(page)

    state.atom("text", "")

    text_ref = ft.Ref[ft.TextField]()

    # Track calls
    existing_handler_calls = []
    atom_values = []

    def existing_handler(e):
        existing_handler_calls.append(e.data)

    state.listen("text", lambda v: atom_values.append(v))

    # Add to page with existing handler
    field = ft.TextField(ref=text_ref, on_change=existing_handler)
    page.add(field)

    # Now bind_two_way (should preserve existing handler)
    state.bind_two_way("text", text_ref)

    # Simulate typing
    class FakeEvent:
        def __init__(self, data):
            self.data = data
            self.control = text_ref.current

    text_ref.current.value = "hello"
    text_ref.current.on_change(FakeEvent("hello"))

    # Both handlers should have been called
    assert state.get("text") == "hello", "Atom should be updated"
    assert "hello" in atom_values, "Listener should be called"
    assert "hello" in existing_handler_calls, "Existing handler should still be called"

    print("✅ Existing handler preserved!")


def test_bind_two_way_multiple_fields():
    """
    Test bind_two_way() with multiple fields (common use case).

    This simulates a form with multiple inputs.
    """
    print("\n=== Test: Multiple Fields ===")

    page = MockPage()
    state = fa.get_state_manager(page)

    # Create atoms for form fields
    state.atom("email", "")
    state.atom("password", "")
    state.atom("name", "")

    # Create refs
    email_ref = ft.Ref[ft.TextField]()
    password_ref = ft.Ref[ft.TextField]()
    name_ref = ft.Ref[ft.TextField]()

    # Add to page
    page.add(
        ft.TextField(ref=email_ref),
        ft.TextField(ref=password_ref),
        ft.TextField(ref=name_ref),
    )

    # Bind all fields
    state.bind_two_way("email", email_ref)
    state.bind_two_way("password", password_ref)
    state.bind_two_way("name", name_ref)

    # Verify all on_change handlers are set
    assert email_ref.current.on_change is not None
    assert password_ref.current.on_change is not None
    assert name_ref.current.on_change is not None

    # Simulate typing in all fields
    class FakeEvent:
        def __init__(self, control, data):
            self.control = control
            self.data = data

    email_ref.current.value = "user@test.com"
    email_ref.current.on_change(FakeEvent(email_ref.current, "user@test.com"))

    password_ref.current.value = "secret123"
    password_ref.current.on_change(FakeEvent(password_ref.current, "secret123"))

    name_ref.current.value = "John Doe"
    name_ref.current.on_change(FakeEvent(name_ref.current, "John Doe"))

    # Verify all atoms updated
    assert state.get("email") == "user@test.com"
    assert state.get("password") == "secret123"
    assert state.get("name") == "John Doe"

    print("✅ Multiple fields test passed!")


if __name__ == "__main__":
    try:
        test_bind_two_way_common_case()
        test_bind_two_way_uncommon_case()
        test_bind_two_way_preserves_existing_handler()
        test_bind_two_way_multiple_fields()

        print("\n" + "=" * 60)
        print("🎉 ALL TESTS PASSED!")
        print("=" * 60)
        print("\nSummary:")
        print("  ✅ Common case (bind AFTER page.add)")
        print("  ✅ Uncommon case (bind BEFORE page.add)")
        print("  ✅ Existing handler preservation")
        print("  ✅ Multiple fields")
        print("=" * 60)

    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback

        traceback.print_exc()
        exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback

        traceback.print_exc()
        exit(1)
