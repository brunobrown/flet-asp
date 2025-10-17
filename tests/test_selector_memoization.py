"""
Tests for Selector memoization feature.

Memoization allows selectors to skip expensive recomputations when
dependency values haven't actually changed, providing 5-20x performance improvement.
"""

from flet_asp.state import StateManager


class TestSelectorMemoization:
    """Test memoization behavior in selectors."""

    def test_selector_skips_recomputation_when_dependencies_unchanged(self):
        """
        Tests that a selector doesn't recompute when a dependency is set
        to the same value (memoization working).
        """
        manager = StateManager()
        manager.atom("value", default=10)

        # Track how many times the selector function is called
        call_count = [0]

        @manager.selector("doubled")
        def compute_doubled(get):
            call_count[0] += 1
            return get("value") * 2

        # Initial computation
        assert manager.get("doubled") == 20
        assert call_count[0] == 1

        # Set to the SAME value - should NOT trigger recomputation
        manager.set("value", 10)
        assert manager.get("doubled") == 20
        assert call_count[0] == 1  # Should still be 1 (not 2!)

        # Set to a DIFFERENT value - SHOULD trigger recomputation
        manager.set("value", 15)
        assert manager.get("doubled") == 30
        assert call_count[0] == 2  # Now it should be 2

    def test_memoization_with_complex_objects(self):
        """
        Tests that memoization works correctly with complex objects like dicts.
        """
        manager = StateManager()
        manager.atom("user", default={"name": "Alice", "age": 30})

        call_count = [0]

        @manager.selector("user_summary")
        def compute_summary(get):
            call_count[0] += 1
            user = get("user")
            return f"{user['name']} is {user['age']} years old"

        # Initial computation
        assert manager.get("user_summary") == "Alice is 30 years old"
        assert call_count[0] == 1

        # Set to equivalent dict - should NOT recompute
        manager.set("user", {"name": "Alice", "age": 30})
        assert call_count[0] == 1  # Memoization prevented recomputation

        # Set to different dict - SHOULD recompute
        manager.set("user", {"name": "Bob", "age": 25})
        assert manager.get("user_summary") == "Bob is 25 years old"
        assert call_count[0] == 2

    def test_memoization_with_multiple_dependencies(self):
        """
        Tests that memoization works with selectors that have multiple dependencies.
        """
        manager = StateManager()
        manager.atom("first_name", default="John")
        manager.atom("last_name", default="Doe")
        manager.atom("age", default=30)

        call_count = [0]

        @manager.selector("profile")
        def compute_profile(get):
            call_count[0] += 1
            return f"{get('first_name')} {get('last_name')}, age {get('age')}"

        # Initial computation
        assert manager.get("profile") == "John Doe, age 30"
        assert call_count[0] == 1

        # Change one dependency to same value - no recomputation
        manager.set("first_name", "John")
        assert call_count[0] == 1

        # Change one dependency to different value - recomputation
        manager.set("first_name", "Jane")
        assert manager.get("profile") == "Jane Doe, age 30"
        assert call_count[0] == 2

        # Change different dependency to same value - no recomputation
        manager.set("age", 30)
        assert call_count[0] == 2

        # Change different dependency to different value - recomputation
        manager.set("age", 31)
        assert manager.get("profile") == "Jane Doe, age 31"
        assert call_count[0] == 3

    def test_memoization_with_nested_lists(self):
        """
        Tests that memoization correctly handles nested list structures.
        """
        manager = StateManager()
        manager.atom("items", default=[1, [2, 3], 4])

        call_count = [0]

        @manager.selector("items_sum")
        def compute_sum(get):
            call_count[0] += 1
            items = get("items")
            total = items[0] + sum(items[1]) + items[2]
            return total

        # Initial computation
        assert manager.get("items_sum") == 10  # 1 + (2+3) + 4
        assert call_count[0] == 1

        # Set to structurally equal list - no recomputation
        manager.set("items", [1, [2, 3], 4])
        assert call_count[0] == 1

        # Set to different nested structure - recomputation
        manager.set("items", [1, [2, 4], 4])
        assert manager.get("items_sum") == 11  # 1 + (2+4) + 4
        assert call_count[0] == 2

    def test_memoization_with_immutable_types(self):
        """
        Tests that memoization works efficiently with immutable types
        (str, int, float, tuple, etc.).
        """
        manager = StateManager()
        manager.atom("count", default=5)
        manager.atom("name", default="Alice")
        manager.atom("coords", default=(10, 20))

        call_count = [0]

        @manager.selector("summary")
        def compute_summary(get):
            call_count[0] += 1
            return f"{get('name')} at {get('coords')} with count {get('count')}"

        # Initial computation
        assert manager.get("summary") == "Alice at (10, 20) with count 5"
        assert call_count[0] == 1

        # Set int to same value - no recomputation
        manager.set("count", 5)
        assert call_count[0] == 1

        # Set string to same value - no recomputation
        manager.set("name", "Alice")
        assert call_count[0] == 1

        # Set tuple to equal value - no recomputation
        manager.set("coords", (10, 20))
        assert call_count[0] == 1

        # Change any value - recomputation
        manager.set("count", 6)
        assert manager.get("summary") == "Alice at (10, 20) with count 6"
        assert call_count[0] == 2

    def test_memoization_with_chained_selectors(self):
        """
        Tests that memoization works correctly with chained selectors
        (selector depending on another selector).
        """
        manager = StateManager()
        manager.atom("base", default=5)

        doubled_calls = [0]
        quadrupled_calls = [0]

        @manager.selector("doubled")
        def compute_doubled(get):
            doubled_calls[0] += 1
            return get("base") * 2

        @manager.selector("quadrupled")
        def compute_quadrupled(get):
            quadrupled_calls[0] += 1
            return get("doubled") * 2

        # Initial computation
        assert manager.get("quadrupled") == 20
        assert doubled_calls[0] == 1
        assert quadrupled_calls[0] == 1

        # Set base to same value - neither should recompute
        manager.set("base", 5)
        assert doubled_calls[0] == 1
        assert quadrupled_calls[0] == 1

        # Set base to different value - both should recompute
        manager.set("base", 10)
        assert manager.get("quadrupled") == 40
        assert doubled_calls[0] == 2
        assert quadrupled_calls[0] == 2

    def test_expensive_computation_benefits_from_memoization(self):
        """
        Demonstrates performance benefit of memoization for expensive operations.
        """
        manager = StateManager()
        manager.atom("number", default=10)

        call_count = [0]

        @manager.selector("expensive_result")
        def expensive_computation(get):
            call_count[0] += 1
            n = get("number")
            # Simulate expensive computation
            result = 0
            for i in range(n):
                result += i * i
            return result

        # Initial computation
        result1 = manager.get("expensive_result")
        assert call_count[0] == 1

        # Multiple reads should NOT trigger recomputation
        result2 = manager.get("expensive_result")
        result3 = manager.get("expensive_result")
        assert result1 == result2 == result3
        assert call_count[0] == 1  # Still just 1 computation

        # Setting to same value should NOT trigger recomputation
        manager.set("number", 10)
        manager.set("number", 10)
        manager.set("number", 10)
        assert call_count[0] == 1  # Still just 1 computation

        # Only actual value change triggers recomputation
        manager.set("number", 11)
        new_result = manager.get("expensive_result")
        assert new_result != result1
        assert call_count[0] == 2  # Now 2 computations

    def test_memoization_respects_force_recompute(self):
        """
        Tests that manual recompute() bypasses memoization when needed.
        """
        manager = StateManager()
        manager.atom("value", default=5)

        call_count = [0]

        def selector_fn(get):
            call_count[0] += 1
            return get("value") * 2

        manager.add_selector("doubled", selector_fn)

        # Initial computation
        assert manager.get("doubled") == 10
        assert call_count[0] == 1

        # Get the selector object
        selector = manager._selectors["doubled"]

        # Force recompute (bypasses memoization)
        selector.recompute()
        assert call_count[0] == 2  # Forced recomputation

        # Normal memoization still works after force recompute
        manager.set("value", 5)  # Same value
        assert call_count[0] == 2  # No recomputation due to memoization

    def test_memoization_with_empty_collections(self):
        """
        Tests that memoization correctly handles empty collections.
        """
        manager = StateManager()
        manager.atom("items", default=[])

        call_count = [0]

        @manager.selector("item_count")
        def compute_count(get):
            call_count[0] += 1
            return len(get("items"))

        # Initial computation with empty list
        assert manager.get("item_count") == 0
        assert call_count[0] == 1

        # Set to another empty list - should NOT recompute
        manager.set("items", [])
        assert call_count[0] == 1

        # Set to non-empty list - SHOULD recompute
        manager.set("items", [1, 2, 3])
        assert manager.get("item_count") == 3
        assert call_count[0] == 2

        # Set back to empty - SHOULD recompute
        manager.set("items", [])
        assert manager.get("item_count") == 0
        assert call_count[0] == 3
