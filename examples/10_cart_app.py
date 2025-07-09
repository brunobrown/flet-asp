import flet as ft
import fasp as fa
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
                on_click=lambda e: on_add({"name": name, "price": price})
            )
        )


def main(page: ft.Page):
    """
    This example demonstrates a shopping cart UI using FASP state management. It includes:
        * A product catalog
        * Cart management with list of items
        * Derived total price and item count
        * Reactive updates using selector() and listen()
        * Cart reset via an async Action
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

    # Selector: total cart price
    @state.selector("total_price")
    def total_price(get):
        return sum(item["price"] for item in get("cart_items"))

    # Selector instance: item count
    item_count_selector = fa.Selector(
        resolve_atom=state.atom,
        select_fn=lambda get: len(get("cart_items"))
    )

    # Async Action: clear all items in the cart
    async def clear_cart(get, set_value, _):
        set_value("cart_items", [])

    clear_cart_action = fa.Action(clear_cart)

    # Add product to cart
    def add_to_cart(item):
        current = state.get("cart_items")
        state.set("cart_items", current + [item])

    # Re-render the cart list when cart changes
    def render_cart_items(_=None):
        items = state.get("cart_items")
        cart_list_ref.current.controls = [
            ft.ListTile(
                title=ft.Text(item["name"]),
                subtitle=ft.Text(f"${item['price']:.2f}")
            )
            for item in items
        ]
        cart_list_ref.current.update()

    # Update item count badge
    def update_count(count):
        item_count_ref.current.value = f"{count} item(s)"
        item_count_ref.current.update()

    # Page UI
    page.title = "🛒 Shopping Cart (FASP)"
    page.add(
        ft.Column([
            ft.Text("🛍️ Products", style=ft.TextThemeStyle.HEADLINE_SMALL),

            # List of products with buttons
            *[ProductCard(p["name"], p["price"], on_add=add_to_cart) for p in products],

            ft.Divider(),

            # Cart section
            ft.Row([
                ft.Text("Cart", style=ft.TextThemeStyle.TITLE_MEDIUM),
                ft.Text(ref=item_count_ref)
            ]),

            ft.Column(ref=cart_list_ref),

            ft.Row([
                ft.Text("Total: "),
                ft.Text(ref=total_text_ref)
            ]),

            ft.OutlinedButton(
                text="Clear Cart",
                on_click=lambda e: page.run_task(clear_cart_action.run_async, state)
            )
        ], width=500)
    )

    # Bind computed selector to UI
    state.bind("total_price", total_text_ref, prop="value")

    # Listeners
    state.listen("cart_items", render_cart_items)
    item_count_selector.listen(callback=update_count)


if __name__ == "__main__":
    ft.app(target=main)
