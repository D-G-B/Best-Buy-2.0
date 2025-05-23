# main.py
import sys
from products import (Product, NonStockedProduct, LimitedProduct,
                      SecondHalfPrice, ThirdOneFree, PercentDiscount)
from store import Store

# ANSI color codes
BLUE = "\033[38;5;39m"
YELLOW = "\033[38;5;220m"
RESET = "\033[0m"
BOLD = "\033[1m"


def print_ascii_banner():
    """Print an ASCII art banner for BEST BUY by DGB"""
    banner = f"""
{BLUE}██████╗ ███████╗███████╗████████╗    ██████╗ ██╗   ██╗██╗   ██╗{RESET}
{BLUE}██╔══██╗██╔════╝██╔════╝╚══██╔══╝    ██╔══██╗██║   ██║╚██╗ ██╔╝{RESET}
{BLUE}██████╔╝█████╗  ███████╗   ██║       ██████╔╝██║   ██║ ╚████╔╝ {RESET}
{BLUE}██╔══██╗██╔══╝  ╚════██║   ██║       ██╔══██╗██║   ██║  ╚██╔╝  {RESET}
{BLUE}██████╔╝███████╗███████║   ██║       ██████╔╝╚██████╔╝   ██║   {RESET}
{BLUE}╚═════╝ ╚══════╝╚══════╝   ╚═╝       ╚═════╝  ╚═════╝    ╚═╝   {RESET}
                                {YELLOW}by DGB{RESET}
"""
    print(banner)


def print_header(text):
    """Print a styled header"""
    border_char = "="
    border_len = 50
    border = BLUE + border_char * border_len + RESET
    print(border)
    print(BLUE + BOLD + text.center(border_len) + RESET)
    print(border)


def display_menu():
    """Display the main menu"""
    print_ascii_banner()
    print(f"\n{YELLOW}Please choose an option:{RESET}")
    print(f"{BLUE}1.{RESET} List all products in store")
    print(f"{BLUE}2.{RESET} Show total amount in store")
    print(f"{BLUE}3.{RESET} Make an order")
    print(f"{BLUE}4.{RESET} Quit")
    print()


def list_products(store_instance):
    """Display all active products in the store"""
    print_header("AVAILABLE PRODUCTS")
    products = store_instance.get_all_products()

    if not products:
        print(f"{YELLOW}No active products available!{RESET}")
        return

    for i, product in enumerate(products, 1):
        print(f"{BLUE}{i}.{RESET} {product.show()}")
    print()


def show_total_quantity(store_instance):
    """Show the total quantity of items in the store"""
    total = store_instance.get_total_quantity()
    print_header("INVENTORY STATUS")
    print(f"{YELLOW}Total number of items in store: {BLUE}{total}{RESET}") #
    print()


def make_order(store_instance):
    """Handle the order process with improved input validation."""
    print_header("NEW ORDER")

    products = store_instance.get_all_products()
    if not products:
        print(f"{YELLOW}No products available to order!{RESET}")
        return

    print(f"{YELLOW}Available products:{RESET}")
    for i, product_item in enumerate(products, 1):
        print(f"{BLUE}{i}.{RESET} {product_item.show()}")

    shopping_list = []
    while True:
        selected_product = None
        # --- Product Selection Loop ---
        while True:
            choice_str = input(
                f"\n{YELLOW}Enter product number (or 0 to finish order): {RESET}"
            ).strip()
            if choice_str == '0':
                break  # Exit product selection, will also break outer loop

            try:
                product_idx = int(choice_str) - 1
                if not (0 <= product_idx < len(products)):
                    print(
                        f"{YELLOW}Invalid product number. Please try again.{RESET}"
                    )
                    continue
                selected_product = products[product_idx]
                break  # Valid product index selected
            except ValueError:
                print(
                    f"{YELLOW}Invalid input. Please enter a number for the product.{RESET}"
                )

        if choice_str == '0':  # User chose to finish order
            break

        # --- Check for Limited Products (e.g., Shipping) already in cart ---
        # This specifically targets products like "Shipping" that can only be added once.
        is_unique_limited_product = (
            isinstance(selected_product, LimitedProduct) and
            selected_product.maximum == 1
        )
        if is_unique_limited_product:
            already_in_cart = False
            for item_in_cart, _ in shopping_list:
                if item_in_cart.name == selected_product.name:
                    already_in_cart = True
                    break
            if already_in_cart:
                print(
                    f"{YELLOW}Warning: '{selected_product.name}' is limited to "
                    f"one per order and is already in your cart. "
                    f"Please choose another product.{RESET}"
                )
                continue  # Go back to asking for a product

        # --- Quantity Input Loop ---
        quantity_to_order = 0
        while True:
            try:
                available_qty_info = ""
                if not isinstance(selected_product, NonStockedProduct):
                    available_qty_info = (
                        f" (Available: {selected_product.get_quantity()})"
                    )

                quantity_str = input(
                    f"{YELLOW}Enter quantity for {selected_product.name}"
                    f"{available_qty_info}: {RESET}"
                ).strip()
                quantity_to_order = int(quantity_str)

                if quantity_to_order <= 0:
                    print(
                        f"{YELLOW}Quantity must be a positive number. "
                        f"Please try again.{RESET}"
                    )
                    continue

                # Check for LimitedProduct maximum for this transaction
                # This check is for items that might have a per-transaction limit
                # different from the "only one ever" type of limit handled above.
                if (isinstance(selected_product, LimitedProduct) and
                        quantity_to_order > selected_product.maximum):
                    print(
                        f"{YELLOW}Error: Cannot order more than "
                        f"{selected_product.maximum} of "
                        f"'{selected_product.name}' at a time. "
                        f"Please try again.{RESET}"
                    )
                    continue

                # Check stock (for stock-managed products)
                if (not isinstance(selected_product, NonStockedProduct) and
                        quantity_to_order > selected_product.get_quantity()):
                    print(
                        f"{YELLOW}Not enough stock for '{selected_product.name}'. "
                        f"Available: {selected_product.get_quantity()}. "
                        f"Please try again.{RESET}"
                    )
                    continue
                break  # Valid quantity entered
            except ValueError:
                print(
                    f"{YELLOW}Invalid input for quantity. "
                    f"Please enter a number.{RESET}"
                )

        # Add to shopping list
        shopping_list.append((selected_product, quantity_to_order))
        print(
            f"{BLUE}Added {quantity_to_order} x {selected_product.name} to your order.{RESET}"
        )

    # Process the order
    if shopping_list:
        try:
            total_price = store_instance.order(shopping_list)
            print_header("ORDER SUMMARY")
            print(
                f"{YELLOW}Order completed! Total price: "
                f"${BLUE}{total_price:.2f}{RESET}"
            )
        except ValueError as e:
            # This catches errors from product.buy() if any pre-checks missed
            # or other logic errors within buy()
            print(
                f"{YELLOW}Error during order processing: {e}. Order cancelled.{RESET}"
            )
    else:
        print(f"{YELLOW}Order cancelled or empty.{RESET}")


def start(store_instance):
    """Main function to start the user interface."""
    while True:
        display_menu()
        try:
            choice = input(f"{YELLOW}Enter your choice (1-4): {RESET}").strip()

            if choice == '1':
                list_products(store_instance)
            elif choice == '2':
                show_total_quantity(store_instance)
            elif choice == '3':
                make_order(store_instance)
            elif choice == '4':
                print_header("THANK YOU FOR SHOPPING WITH US")
                print(f"{YELLOW}Goodbye!{RESET}")
                sys.exit(0)
            else:
                # Handles cases where choice is not 1-4, including empty input
                raise ValueError("Invalid choice")
        except ValueError:
            print(
                f"{YELLOW}Invalid choice. Please enter a number between 1 and 4.{RESET}"
            )

        input(f"\n{BLUE}Press Enter to continue...{RESET}")


def main():
    """Initialises store and starts user interface."""
    # Setup initial stock of inventory
    product_list = [
        Product("MacBook Air M2", price=1450, quantity=100),
        Product("Bose QuietComfort Earbuds", price=250, quantity=500),
        Product("Google Pixel 7", price=500, quantity=250),
        NonStockedProduct("Windows License", price=125),
        LimitedProduct("Shipping", price=10, quantity=250, maximum=1) # Max 1 per order
    ]

    # Create promotion catalog
    second_half_price = SecondHalfPrice("Second Half price!")
    third_one_free = ThirdOneFree("Third One Free!")
    thirty_percent = PercentDiscount("30% off!", percent=30)

    # Add promotions to products
    if len(product_list) > 3:  # Check to prevent IndexError
        product_list[0].set_promotion(second_half_price)
        product_list[1].set_promotion(third_one_free)
        product_list[3].set_promotion(thirty_percent)
    else:
        print(f"{YELLOW}Warning: Product list is shorter than expected for promotions.{RESET}")

    # Initialize the store with the prepared list of products and begin the interactive user interface.
    store_instance = Store(product_list)
    start(store_instance)


if __name__ == '__main__':
    main()