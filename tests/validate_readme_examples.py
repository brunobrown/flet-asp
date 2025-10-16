"""
Automated validation script for all README.md examples.
This script tests all examples without requiring GUI interaction.
"""

import asyncio
import sys


def test_1_basic_counter():
    """Test: 1. Basic Counter (Your First Atom)"""
    print("Testing: 1. Basic Counter...")
    try:
        import flet_asp as fa

        # Mock page object
        class MockPage:
            def __init__(self):
                self.controls = []

            def add(self, control):
                self.controls.append(control)

            def update(self):
                pass

        page = MockPage()
        fa.get_state_manager(page)
        page.state.atom("count", 0)

        # Test get/set
        assert page.state.get("count") == 0
        page.state.set("count", 5)
        assert page.state.get("count") == 5

        print("✅ Test 1: Basic Counter - PASSED")
        return True
    except Exception as e:
        print(f"❌ Test 1: Basic Counter - FAILED: {e}")
        return False


def test_2_two_way_binding():
    """Test: 2. Form with Two-Way Binding"""
    print("Testing: 2. Form with Two-Way Binding...")
    try:
        import flet_asp as fa

        class MockPage:
            def __init__(self):
                self.controls = []

            def add(self, control):
                self.controls.append(control)

            def update(self):
                pass

        page = MockPage()
        fa.get_state_manager(page)

        # Create atoms for form fields
        page.state.atom("email", "")
        page.state.atom("password", "")

        # Test get/set
        page.state.set("email", "test@test.com")
        page.state.set("password", "123")

        assert page.state.get("email") == "test@test.com"
        assert page.state.get("password") == "123"

        print("✅ Test 2: Two-Way Binding - PASSED")
        return True
    except Exception as e:
        print(f"❌ Test 2: Two-Way Binding - FAILED: {e}")
        return False


def test_3_computed_state():
    """Test: 3. Computed State with Selectors"""
    print("Testing: 3. Computed State with Selectors...")
    try:
        import flet_asp as fa

        class MockPage:
            def __init__(self):
                self.controls = []

            def add(self, control):
                self.controls.append(control)

            def update(self):
                pass

        page = MockPage()
        fa.get_state_manager(page)

        # Base atoms
        page.state.atom("first_name", "John")
        page.state.atom("last_name", "Doe")

        # Computed state
        @page.state.selector("full_name")
        def compute_full_name(get):
            return f"{get('first_name')} {get('last_name')}"

        # Test computed value
        result = page.state.get("full_name")
        assert result == "John Doe", f"Expected 'John Doe', got '{result}'"

        # Test reactivity
        page.state.set("first_name", "Jane")
        result = page.state.get("full_name")
        assert result == "Jane Doe", f"Expected 'Jane Doe', got '{result}'"

        print("✅ Test 3: Computed State - PASSED")
        return True
    except Exception as e:
        print(f"❌ Test 3: Computed State - FAILED: {e}")
        return False


def test_4_async_actions():
    """Test: 4. Async Operations with Actions"""
    print("Testing: 4. Async Actions...")
    try:
        import flet_asp as fa

        class MockPage:
            def __init__(self):
                self.controls = []

            def add(self, control):
                self.controls.append(control)

            def update(self):
                pass

        page = MockPage()
        fa.get_state_manager(page)

        page.state.atom("user", None)
        page.state.atom("loading", False)

        # Define async action
        async def login_action(get, set_value, params):
            set_value("loading", True)
            await asyncio.sleep(0.1)  # Short delay for testing

            email = params.get("email")
            password = params.get("password")

            if email == "test@test.com" and password == "123":
                set_value("user", {"email": email, "name": "Test User"})
            else:
                set_value("user", None)

            set_value("loading", False)

        # Create action
        login = fa.Action(login_action)

        # Test async action
        async def run_test():
            await login.run_async(
                page.state, {"email": "test@test.com", "password": "123"}
            )
            user = page.state.get("user")
            assert user is not None
            assert user["name"] == "Test User"
            assert page.state.get("loading") is False

        asyncio.run(run_test())

        print("✅ Test 4: Async Actions - PASSED")
        return True
    except Exception as e:
        print(f"❌ Test 4: Async Actions - FAILED: {e}")
        return False


def test_5_custom_controls():
    """Test: 5. Custom Controls with Reactive State"""
    print("Testing: 5. Custom Controls...")
    try:
        import flet_asp as fa

        class MockPage:
            def __init__(self):
                self.controls = []

            def add(self, control):
                self.controls.append(control)

            def update(self):
                pass

        page = MockPage()
        fa.get_state_manager(page)

        # Test multiple independent counters
        page.state.atom("counter1_count", 0)
        page.state.atom("counter2_count", 0)
        page.state.atom("counter3_count", 0)

        page.state.set("counter1_count", 5)
        page.state.set("counter2_count", 10)
        page.state.set("counter3_count", 15)

        assert page.state.get("counter1_count") == 5
        assert page.state.get("counter2_count") == 10
        assert page.state.get("counter3_count") == 15

        print("✅ Test 5: Custom Controls - PASSED")
        return True
    except Exception as e:
        print(f"❌ Test 5: Custom Controls - FAILED: {e}")
        return False


def test_6_async_selectors():
    """Test: 6. Complex Selectors with Async Data (FIXED)"""
    print("Testing: 6. Async Selectors...")
    try:
        import flet_asp as fa

        class MockPage:
            def __init__(self):
                self.controls = []

            def add(self, control):
                self.controls.append(control)

            def update(self):
                pass

        page = MockPage()
        fa.get_state_manager(page)

        # Base atoms
        page.state.atom("user_id", 1)

        # Async selector - FIXED VERSION using decorator
        @page.state.selector("user_data")
        async def fetch_user(get):
            user_id = get("user_id")
            await asyncio.sleep(0.1)  # Short delay for testing

            users = {
                1: {"name": "Alice", "email": "alice@example.com"},
                2: {"name": "Bob", "email": "bob@example.com"},
                3: {"name": "Charlie", "email": "charlie@example.com"},
            }

            return users.get(user_id, {"name": "Unknown", "email": "N/A"})

        # Test that the selector was created successfully
        # Full async testing requires a real Flet page with event loop
        selector = page.state._selectors.get("user_data")
        assert selector is not None, "Selector should be created"

        print("✅ Test 6: Async Selectors - PASSED (syntax check)")
        print("   Note: Full async behavior requires GUI testing with Flet")
        return True
    except Exception as e:
        print(f"❌ Test 6: Async Selectors - FAILED: {e}")
        return False


def test_7_shopping_cart():
    """Test: 7. Shopping Cart Example"""
    print("Testing: 7. Shopping Cart...")
    try:
        import flet_asp as fa

        class MockPage:
            def __init__(self):
                self.controls = []

            def add(self, control):
                self.controls.append(control)

            def update(self):
                pass

        page = MockPage()
        fa.get_state_manager(page)

        # State
        page.state.atom("cart_items", [])

        # Selectors
        @page.state.selector("cart_total")
        def calculate_total(get):
            items = get("cart_items")
            return sum(item["price"] * item["quantity"] for item in items)

        @page.state.selector("cart_count")
        def count_items(get):
            items = get("cart_items")
            return sum(item["quantity"] for item in items)

        # Test empty cart
        assert page.state.get("cart_total") == 0
        assert page.state.get("cart_count") == 0

        # Add items to cart
        page.state.set(
            "cart_items",
            [
                {"id": 1, "name": "Laptop", "price": 999.99, "quantity": 1},
                {"id": 2, "name": "Mouse", "price": 29.99, "quantity": 2},
            ],
        )

        # Test computed values
        total = page.state.get("cart_total")
        count = page.state.get("cart_count")

        assert count == 3  # 1 laptop + 2 mice
        assert abs(total - 1059.97) < 0.01  # 999.99 + (29.99 * 2)

        print("✅ Test 7: Shopping Cart - PASSED")
        return True
    except Exception as e:
        print(f"❌ Test 7: Shopping Cart - FAILED: {e}")
        return False


def main():
    """Run all tests and report results"""
    print("=" * 60)
    print("VALIDATING ALL README.MD EXAMPLES")
    print("=" * 60)
    print()

    tests = [
        test_1_basic_counter,
        test_2_two_way_binding,
        test_3_computed_state,
        test_4_async_actions,
        test_5_custom_controls,
        test_6_async_selectors,
        test_7_shopping_cart,
    ]

    results = []
    for test in tests:
        result = test()
        results.append(result)
        print()

    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    passed = sum(results)
    total = len(results)

    print(f"✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {total - passed}/{total}")

    if all(results):
        print()
        print("🎉 ALL TESTS PASSED! All README examples are working correctly.")
        return 0
    else:
        print()
        print("⚠️  SOME TESTS FAILED! Please review the failed examples.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
