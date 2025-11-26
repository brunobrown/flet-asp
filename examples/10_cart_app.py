import flet as ft
import flet_asp as fa
from typing import Callable


class ProductCard(ft.Card):
    """
    A visual card for displaying a product with 'Add to Cart' button.
    """

    def __init__(self, name: str, price: float, on_add: Callable):
        super().__init__()
        self.content = ft.ListTile(
            title=ft.Text(name),
            subtitle=ft.Text(f"${price:.2f}"),
            trailing=ft.IconButton(
                icon=ft.Icons.ADD_SHOPPING_CART,
                on_click=lambda e: on_add({"name": name, "price": price}),
            ),
        )


def main(page: ft.Page):
    """
    This example demonstrates a shopping cart UI using Flet-ASP state management.

    Key concepts demonstrated:
        * @selector decorator for derived state (total price, item count)
        * @action decorator for async operations (clear cart)
        * listen() for dynamic control list rendering
        * bind() for simple value updates

    The app includes:
        * A product catalog
        * Cart management with list of items
        * Derived total price and item count (using selectors)
        * Cart reset via @action decorator
    """

    state = fa.get_state_manager(page)

    # Reactive atoms
    state.atom("cart_items", [])

    # UI references
    cart_list_ref = ft.Ref[ft.Column]()
    total_text_ref = ft.Ref[ft.Text]()
    item_count_ref = ft.Ref[ft.Text]()

    # Static product list
    products = [
        {"name": "Laptop", "price": 3500.0},
        {"name": "Mouse", "price": 150.0},
        {"name": "Keyboard", "price": 300.0},
    ]

    # Selector: total cart price (formatted as string for display)
    @state.selector("total_price")
    def compute_total_price(get):
        total = sum(item["price"] for item in get("cart_items"))
        return f"${total:.2f}"

    # Selector: item count (formatted as string for display)
    @state.selector("item_count")
    def compute_item_count(get):
        count = len(get("cart_items"))
        return f"{count} item(s)"

    # Action: clear all items in the cart using @action decorator
    @state.action
    async def clear_cart(_get, set_value):
        set_value("cart_items", [])

    # Add product to cart (creates new list for immutability)
    def add_to_cart(item):
        current = state.get("cart_items")
        state.set("cart_items", [*current, item])

    # Re-render the cart list when cart changes
    def render_cart_items(_=None):
        """
        Render cart items list.

        Note: This uses control.update() because we're dynamically creating
        a list of controls. For simple value bindings, use state.bind() instead.
        """
        items = state.get("cart_items")
        cart_list_ref.current.controls = [
            ft.ListTile(
                title=ft.Text(item["name"]), subtitle=ft.Text(f"${item['price']:.2f}")
            )
            for item in items
        ]
        # Update only this control - required for dynamic control lists
        cart_list_ref.current.update()

    # Page UI
    page.title = "🛒 Shopping Cart (Flet-ASP)"
    page.add(
        ft.Column(
            [
                ft.Text("🛍️ Products", style=ft.TextThemeStyle.HEADLINE_SMALL),
                # List of products with buttons
                *[
                    ProductCard(p["name"], p["price"], on_add=add_to_cart)
                    for p in products
                ],
                ft.Divider(),
                # Cart section
                ft.Row(
                    [
                        ft.Text("Cart", style=ft.TextThemeStyle.TITLE_MEDIUM),
                        ft.Text(ref=item_count_ref),
                    ]
                ),
                ft.Column(ref=cart_list_ref),
                ft.Row([ft.Text("Total: "), ft.Text(ref=total_text_ref)]),
                ft.OutlinedButton(
                    text="Clear Cart",
                    on_click=lambda e: page.run_task(clear_cart),
                ),
            ],
            width=500,
        )
    )

    # Bind selectors to UI - fully declarative, no manual update needed!
    state.bind("total_price", total_text_ref, prop="value")
    state.bind("item_count", item_count_ref, prop="value")

    # Listen for cart changes to render dynamic list
    state.listen("cart_items", render_cart_items, immediate=False)


if __name__ == "__main__":
    ft.app(target=main)
