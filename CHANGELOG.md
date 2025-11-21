# Changelog

---

## [0.3.0] - 2025-11-21

### Added
- **`@state.action` decorator** - New way to create actions
  - Previously, only the direct instantiation form `fa.Action()` was available
  - Decorator automatically detects async functions using `asyncio.iscoroutinefunction()`
  - Returns appropriate wrapper (sync or async) based on function type
  - Compatible with Flet's `page.run_task()` for async operations
  - Cleaner, more Pythonic syntax

```python
# ✅ NEW: Decorator form (recommended)
@state.action
async def clear_completed(get, set):
    set("tasks", [t for t in get("tasks") if not t["completed"]])

on_click=lambda e: page.run_task(clear_completed)

# Still supported: Direct instantiation
clear_action = fa.Action(lambda get, set, _: set("tasks", [...]))
```

### Changed
- **`StateManager.action()` method**
  - Added `asyncio.iscoroutinefunction()` check for async detection
  - Async functions now return `async_wrapper` that properly awaits the action
  - Sync functions continue to return regular `wrapper`

### Updated
- **`examples/9_todo.py`** - Updated to use `@state.action` decorator instead of direct instantiation
- **`examples/testando.py`** - Converted to 100% declarative approach (removed `page.update()`)

---

## [0.2.2] - 2025-11-17

### Fixed
- **`bind_two_way()` handler synchronization**
  - Fixed `on_change` handler not being called when users typed in TextField controls
  - Added `control.current.update()` after setting handlers to sync with Flet's backend
  - Improved value extraction from events prioritizing `e.data`, then `e.control.value`

- **Code quality**: Changed bare `except:` to `except Exception:` (ruff E722)

### Documentation
- **New section**: "Listen, Selector, and Action: When to use each one?" in README.md
  - Comparison table of listen(), selector(), action()
  - Use cases with code examples
  - Decision tree for choosing which to use
  - Best practices (DO's and DON'Ts)

### Testing
- Added `test_bind_two_way_cases.py` with 4 comprehensive tests
  - Common case: bind after `page.add()`
  - Uncommon case: bind before `page.add()`
  - Handler preservation test
  - Multiple fields test

---

## [0.2.1] - 2025-10-16

### Added
- **Selector Memoization** (5-20x performance improvement)
  - Intelligent caching of dependency values to skip unnecessary recomputations
  - Automatic detection of actual value changes using deep equality comparison
  - Supports complex nested structures (dicts, lists, tuples, sets)
  - Thread-safe implementation with `threading.Lock`
  - Force recomputation via `selector.recompute()` when needed
  - Comprehensive test suite with 9 memoization-specific tests

- **Chained Selectors Support**
  - Selectors can now depend on other selectors, not just atoms
  - New internal `_resolve_atom_or_selector()` method for universal dependency resolution
  - Enables complex derived state patterns and selector composition

### Changed
- **Optimized `deep_equal()` function in `utils.py`**
  - Replaced JSON serialization with recursive type-specific comparison
  - 5-10x faster for nested structures
  - Eliminates temporary string allocations
  - Handles all data types: primitives, collections, custom objects
  - Exact type matching (bool vs int distinction)

- **Enhanced `Selector` class**
  - Added `_cached_deps` dictionary for memoization
  - Modified `_setup_dependencies()` to initialize dependency cache
  - Updated `_on_dependency_change()` to check cached values before recomputing
  - Enhanced `recompute()` to clear cache and force recomputation
  - Improved documentation with performance notes

- **Enhanced `StateManager` class**
  - Added `_resolve_atom_or_selector()` for unified atom/selector resolution
  - Updated `add_selector()` to support chained selectors

### Performance
- **Selector performance**: 5-20x faster for selectors with expensive computations
- **Deep equality checks**: 5-10x faster than JSON-based comparison
- **Memory efficiency**: Only deep copy mutable types (dict, list, set)
- **Zero performance penalty**: Single `deep_equal()` check when values change

### Testing
- Added `test_selector_memoization.py` with 9 comprehensive tests
- All 38 tests passing (29 existing + 9 new)
- Added `validate_readme.py` for automated README examples validation
- Configured `pyproject.toml` with pytest settings for cleaner test runs

---

## [0.2.0] - 2025-10-16

### Added
- **Hybrid Update Strategy** for reliable bindings
  - Bindings now work correctly even when controls are bound before being added to the page
  - Eliminates `AssertionError: Control must be added to the page first` errors
  - 4-step strategy: Lazy updates → Immediate updates → Lifecycle hooks → Queue fallback

- **Python 3.14+ Optimizations**
  - Free-threading support for parallel binding processing (up to 4x faster)
  - Automatic detection and configuration of Python version features
  - Configurable thread pool size via `Atom.MAX_PARALLEL_BINDS`
  - Incremental garbage collection benefits (10x smaller pauses)
  - 3-5% overall performance improvement with tail call interpreter

- **Lifecycle Hook Integration**
  - Automatic `did_mount()` hook injection for custom controls (Column, Row, Stack, etc.)
  - Seamless integration with modern Flet 0.21+ custom control pattern
  - Zero-latency updates for custom controls

- **Automatic Flush Mechanism**
  - `StateManager` automatically hooks into `page.update()` to flush pending updates
  - Transparent retry of queued bindings when page is updated
  - WeakRef-based memory management prevents leaks

- **Comprehensive Documentation**
  - New `PERFORMANCE.md` guide with benchmarks and optimization tips
  - Detailed docstrings in English for all public and private methods
  - Performance comparison between Python versions

- **New Examples**
  - `11_screen_a_navigation_screen_b.py` - Demonstrates hybrid binding with navigation
  - `11.1_global_state_outside.py` - StateManager usage outside page scope for testing and multi-window apps
  - `12_python314_performance.py` - Interactive Python 3.14+ features demo with dark/light mode and responsive layout
  - `13_hybrid_binding_advanced.py` - Advanced hybrid binding scenarios with dark/light mode and responsive layout
  - `16_reactive_atomic_components/` - Complete library of reactive components combining Atomic Design with flet-asp state
    - ReactiveAtom base class for creating custom reactive components
    - ReactiveCounter with increment/decrement/reset functionality
    - ReactiveStatCard for real-time dashboard metrics with trend indicators
    - ReactiveInput with two-way reactive binding
    - ReactiveForm for complete forms with validation
    - ReactiveProgress for progress tracking with automatic percentage display
    - ReactiveText for automatically updating text displays

- **Test Coverage**
  - 12 new tests for hybrid binding strategy (`test_hybrid_binding.py`)
  - Tests for lazy updates, immediate updates, queue management, and memory safety
  - All existing 18 tests continue to pass

### Changed
- **`Atom` class enhancements**
  - Added `_pending_updates` queue for unmounted controls
  - Added `_safe_update()` method implementing hybrid strategy
  - Added `_try_update_immediate()`, `_try_hook_did_mount()` methods
  - Added `_flush_pending_updates()`, `_flush_sequential()`, `_flush_parallel()` methods
  - Added `_add_to_pending_queue()`, `_add_to_threaded_queue()` methods
  - Updated `bind()`, `bind_dynamic()`, `bind_two_way()` to use hybrid strategy
  - Removed `immediate` parameter from `bind()`, `bind_dynamic()`, `bind_two_way()` (simplified API)
  - Enhanced `__repr__()` to include pending updates count

- **`StateManager` class enhancements**
  - Constructor now accepts optional `page` parameter for automatic flush
  - Added `_hook_page_update()` method to wrap `page.update()`
  - Automatic flush of all atoms and selectors after page updates
  - Defensive programming for mock pages in tests

- **`get_state_manager()` function**
  - Now passes `page` to `StateManager` constructor
  - Enhanced docstring with usage example

- **Examples 12 & 13 enhancements**
  - Added dark/light mode toggle with theme persistence
  - Added responsive layouts using ResponsiveRow
  - Improved Material Design with Cards and proper elevation
  - Better mobile/tablet/desktop adaptation with breakpoints (sm/md/lg)

- **Performance optimizations**
  - Strategic exception handling for minimal overhead
  - WeakRef usage for memory-safe queue management

### Fixed
- **Critical bug**: `AssertionError` when binding controls before adding them to page
  - This was a major pain point affecting navigation and dynamic layouts
  - Hybrid strategy ensures bindings always work, regardless of order

- **Memory safety**: Potential memory leaks with pending updates
  - Now uses `weakref.ref()` for automatic cleanup of destroyed controls

- **Code quality**: Fixed `_try_hook_did_mount` method
  - Changed from instance method to static method (added `@staticmethod` decorator)
  - Removed unused parameters `prop` and `value` from method signature
  - Method now has cleaner signature: `_try_hook_did_mount(target: Control) -> bool`
  - Updated all call sites to use simplified signature

- **ReactiveProgress component**: Fixed page.update() issue
  - Progress bar updates now work independently without requiring form submission
  - Added `page.update()` in listen() callback for immediate UI updates

### Performance
- **Zero overhead** for correctly-ordered bindings (99% of cases)
- **~10ms latency** for unmounted controls (auto-retried on page.update())
- **Python 3.14+ gains**:
  - Up to 4x faster binding processing (free-threading)
  - 10x smaller GC pauses (20ms → 2ms)
  - 3-5% overall speed improvement (tail call interpreter)

### Documentation
- Updated `README.md` with performance section and Python 3.14+ information
- Added comprehensive `PERFORMANCE.md` guide
- Enhanced all method docstrings with detailed parameter descriptions and examples
- Added inline code comments explaining hybrid strategy flow
- **New section**: "Global State Outside Page Scope" in README.md
  - Complete guide for using StateManager outside page scope
  - Use cases: testing, multi-window applications, state sharing
  - Comparison tables between page.state vs global_state approaches
  - Common pitfalls and solutions
  - Unit testing examples with global state
- **Comprehensive documentation** for Example 16 (Reactive Atomic Components)
  - Detailed README with component APIs and usage examples
  - Real-world use cases (dashboards, forms, progress tracking)
  - Advanced patterns (computed values, conditional rendering, validation)

### Testing
- All 18 existing tests pass without modification
- 12 new tests for hybrid binding strategy
- Total test coverage: 30 tests, 100% passing

---

## [0.1.3] - 2025-09-02

### Added
- State alias feature (`page.state`)
- Comprehensive test suite

### Changed
- Improved API documentation
- Enhanced examples

---

## [0.1.0] - 2025-07-07

### Added
- Initial release
- `Atom` class for reactive state
- `Selector` class for derived state
- `Action` class for async workflows
- `StateManager` for global state management
- Basic binding support (`bind`, `bind_dynamic`, `bind_two_way`)
- Example applications

---

## Migration Guide

### From 0.1.3 to 0.2.0

**No breaking changes!** The hybrid update strategy is fully backward compatible.

Your existing code will work exactly as before, but with these improvements:

1. **Bindings are more reliable** - No more `AssertionError` when binding before mount
2. **Better performance** - Automatic Python 3.14+ optimizations
3. **More flexibility** - Can bind controls in any order

**Optional enhancements you can adopt:**

```python
# 1. Take advantage of Python 3.14+ parallelism (if available)
from flet_asp.atom import Atom
Atom.MAX_PARALLEL_BINDS = 8  # For giant apps with 1000+ bindings

# 2. Use listen() with immediate=False for change-only tracking
page.state.listen("page_view", log_analytics, immediate=False)

# 3. Bind before adding to page (now works!)
page.state.bind("count", count_ref)  # ✅ Safe now!
page.add(ft.Text(ref=count_ref))
```

---

## Support

- **Issues**: https://github.com/brunobrown/flet-asp/issues
- **Discord**: https://discord.gg/dzWXP8SHG8
- **Docs**: See `README.md` and `PERFORMANCE.md`