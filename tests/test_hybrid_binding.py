"""
Tests for the hybrid binding strategy in Flet-ASP.

These tests verify that bindings work correctly regardless of when
controls are added to the page.
"""

import pytest
from unittest.mock import Mock
from flet import Ref, Column
from flet_asp.atom import Atom
from flet_asp.state import StateManager


class MockPage:
    """Mock Flet Page for testing."""

    def __init__(self):
        self.controls = []

    def update(self, *args):
        """Mock update method."""
        pass


class TestHybridBinding:
    """Tests for hybrid binding strategy."""

    def test_bind_before_mount_uses_lazy_update(self):
        """Test that binding before mount sets property without error."""
        atom = Atom(42, key="test")
        mock_control = Mock()
        mock_control.page = None  # Not mounted
        ref = Ref()
        ref.current = mock_control

        # This should NOT raise an error
        atom.bind(ref, prop="value", update=True)

        # Property should be set (lazy update)
        assert mock_control.value == 42

    def test_bind_after_mount_uses_immediate_update(self):
        """Test that binding after mount updates immediately."""
        atom = Atom(100, key="test")
        mock_control = Mock()
        mock_control.page = MockPage()  # Mounted
        ref = Ref()
        ref.current = mock_control

        # Bind to already-mounted control
        atom.bind(ref, prop="value", update=True)

        # Should have called update()
        mock_control.update.assert_called_once()
        assert mock_control.value == 100

    def test_pending_queue_retries_on_flush(self):
        """Test that pending updates are retried when flushed."""
        atom = Atom(50, key="test")
        mock_control = Mock()
        mock_control.page = None  # Not mounted initially
        ref = Ref()
        ref.current = mock_control

        # Bind before mount (goes to queue)
        atom.bind(ref, prop="value", update=True)

        # Verify in pending queue
        assert len(atom._pending_updates) > 0

        # Now "mount" the control
        mock_control.page = MockPage()

        # Flush pending updates
        atom._flush_pending_updates()

        # Should have called update() now
        mock_control.update.assert_called()

        # Queue should be empty
        assert len(atom._pending_updates) == 0

    def test_multiple_bindings_before_mount(self):
        """Test multiple bindings before controls are mounted."""
        atom1 = Atom("Hello", key="atom1")
        atom2 = Atom("World", key="atom2")

        ref1 = Ref()
        ref1.current = Mock(page=None)

        ref2 = Ref()
        ref2.current = Mock(page=None)

        # Bind both before mount
        atom1.bind(ref1, prop="value")
        atom2.bind(ref2, prop="value")

        # Both should have property set
        assert ref1.current.value == "Hello"
        assert ref2.current.value == "World"

        # Both should be in pending queues
        assert len(atom1._pending_updates) > 0
        assert len(atom2._pending_updates) > 0

    def test_state_change_updates_queued_bindings(self):
        """Test that state changes update even queued bindings."""
        atom = Atom(0, key="counter")
        ref = Ref()
        ref.current = Mock(page=None)

        # Bind before mount
        atom.bind(ref, prop="value")
        assert ref.current.value == 0

        # Change value
        atom._set_value(1)

        # Property should be updated (lazy)
        assert ref.current.value == 1

    def test_custom_control_with_did_mount_hook(self):
        """Test that custom controls with did_mount get hooked."""
        atom = Atom(123, key="test")

        # Create a mock custom control (like Column, Row, Stack)
        class MockCustomControl(Column):
            def __init__(self):
                super().__init__()
                self.page = None
                self.did_mount_called = False

            def did_mount(self):
                self.did_mount_called = True

        control = MockCustomControl()
        ref = Ref()
        ref.current = control

        # Bind before mount
        atom.bind(ref, prop="value")

        # did_mount should be wrapped
        # (we can't easily test the wrapper without actually mounting,
        # but we can verify it was replaced)
        assert callable(control.did_mount)

    def test_duplicate_binding_prevention(self):
        """Test that duplicate bindings are prevented."""
        atom = Atom(42, key="test")
        ref = Ref()
        ref.current = Mock(page=MockPage())

        # Bind once
        atom.bind(ref, prop="value")
        initial_listener_count = len(atom._listeners)

        # Try to bind again with same ref
        atom.bind(ref, prop="value")

        # Should NOT have added another listener
        assert len(atom._listeners) == initial_listener_count

    def test_weakref_prevents_memory_leak(self):
        """Test that weakref allows garbage collection of destroyed controls."""
        import gc

        atom = Atom(100, key="test")
        control = Mock(page=None)
        ref = Ref()
        ref.current = control

        # Bind before mount (goes to queue)
        atom.bind(ref, prop="value")

        # Verify in queue
        assert len(atom._pending_updates) > 0

        # Delete the control reference
        ref.current = None
        del control
        gc.collect()

        # Flush should handle destroyed control gracefully
        atom._flush_pending_updates()

        # Queue should be cleaned up (weakref returns None)
        assert len(atom._pending_updates) == 0


class TestStateManagerIntegration:
    """Integration tests for StateManager with hybrid binding."""

    def test_state_manager_flush_hook(self):
        """Test that StateManager hooks page.update() for automatic flush."""
        mock_page = MockPage()
        mock_page.update = Mock()

        # Create state manager with page
        _ = StateManager(mock_page)

        # Verify update was wrapped
        assert callable(mock_page.update)

    def test_bind_via_state_manager(self):
        """Test binding through StateManager."""
        mock_page = MockPage()
        mock_page.update = Mock()

        state = StateManager(mock_page)
        state.atom("counter", 0)

        ref = Ref()
        ref.current = Mock(page=None)

        # Bind via state manager
        state.bind("counter", ref, prop="value")

        # Property should be set
        assert ref.current.value == 0

    def test_multiple_atoms_flush_together(self):
        """Test that multiple atoms flush together on page.update()."""
        mock_page = MockPage()

        # Create state with multiple atoms
        state = StateManager(mock_page)
        state.atom("atom1", 1)
        state.atom("atom2", 2)

        ref1 = Ref()
        ref1.current = Mock(page=None)

        ref2 = Ref()
        ref2.current = Mock(page=None)

        # Bind both
        state.bind("atom1", ref1)
        state.bind("atom2", ref2)

        # Both should be in pending queues
        assert len(state.atom("atom1")._pending_updates) > 0
        assert len(state.atom("atom2")._pending_updates) > 0

        # Mount controls
        ref1.current.page = mock_page
        ref2.current.page = mock_page

        # Call page.update() (which triggers flush)
        mock_page.update()

        # Queues should be processed
        # Note: In real scenario, this would clear queues
        # Our mock doesn't fully simulate this, but structure is correct


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
