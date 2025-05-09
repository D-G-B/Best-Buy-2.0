import sys
from products import Product, NonStockedProduct, LimitedProduct, SecondHalfPrice, ThirdOneFree, PercentDiscount
from store import Store


# ANSI color codes
BLUE = "\033[38;5;39m"  # Lighter blue
YELLOW = "\033[38;5;220m"
RESET = "\033[0m"
BOLD = "\033[1m"

# setup initial stock of inventory
product_list = [ Product("MacBook Air M2", price=1450, quantity=100),
                 Product("Bose QuietComfort Earbuds", price=250, quantity=500),
                 Product("Google Pixel 7", price=500, quantity=250),
                 NonStockedProduct("Windows License", price=125),
                 LimitedProduct("Shipping", price=10, quantity=250, maximum=1)
               ]

# Create promotion catalog
second_half_price = SecondHalfPrice("Second Half price!")
third_one_free = ThirdOneFree("Third One Free!")
thirty_percent = PercentDiscount("30% off!", percent=30)

# Add promotions to products
product_list[0].set_promotion(second_half_price)
product_list[1].set_promotion(third_one_free)
product_list[3].set_promotion(thirty_percent)

best_buy = Store(product_list)


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
    """Print a styled header in LIDL colors"""
    border = BLUE + "=" * 50 + RESET
    print(border)
    print(BLUE + BOLD + text.center(50) + RESET)
    print(border)


def display_menu():
    """Display the main menu with LIDL colors"""
    print_ascii_banner()
    print(f"\n{YELLOW}Please choose an option:{RESET}")
    print(f"{BLUE}1.{RESET} List all products in store")
    print(f"{BLUE}2.{RESET} Show total amount in store")
    print(f"{BLUE}3.{RESET} Make an order")
    print(f"{BLUE}4.{RESET} Quit")
    print()


def list_products(store):
    """Display all active products in the store"""
    print_header("AVAILABLE PRODUCTS")
    products = store.get_all_products()

    if not products:
        print(f"{YELLOW}No active products available!{RESET}")
        return

    for i, product in enumerate(products, 1):
        print(f"{BLUE}{i}.{RESET} {product.show()}")
    print()


def show_total_quantity(store):
    """Show the total quantity of items in the store"""
    total = store.get_total_quantity()
    print_header("INVENTORY STATUS")
    print(f"{YELLOW}Total number of items in store: {BLUE}{total}{RESET}")
    print()


def make_order(store):
    """Handle the order process"""
    print_header("NEW ORDER")

    # First show available products
    products = store.get_all_products()
    if not products:
        print(f"{YELLOW}No products available to order!{RESET}")
        return

    print(f"{YELLOW}Available products:{RESET}")
    for i, product in enumerate(products, 1):
        print(f"{BLUE}{i}.{RESET} {product.show()}")

    # Create shopping list
    shopping_list = []
    try:
        while True:
            choice = input(f"\n{YELLOW}Enter product number (or 0 to finish order): {RESET}")
            if choice == '0':
                break

            product_idx = int(choice) - 1
            if product_idx < 0 or product_idx >= len(products):
                print(f"{YELLOW}Invalid product number. Please try again.{RESET}")
                continue

            quantity = int(input(f"{YELLOW}Enter quantity to order: {RESET}"))

            try:
                # Check if quantity is valid before adding to shopping list
                if quantity <= products[product_idx].get_quantity():
                    shopping_list.append((products[product_idx], quantity))
                    print(f"{BLUE}Added {quantity} x {products[product_idx].name} to your order{RESET}")
                else:
                    print(
                        f"{YELLOW}Not enough stock available. Maximum available: {products[product_idx].get_quantity()}{RESET}")
            except ValueError as e:
                print(f"{YELLOW}Error: {e}{RESET}")

        # Process the order if shopping list is not empty
        if shopping_list:
            total_price = store.order(shopping_list)
            print_header("ORDER SUMMARY")
            print(f"{YELLOW}Order completed! Total price: ${BLUE}{total_price:.2f}{RESET}")
        else:
            print(f"{YELLOW}Order cancelled or empty.{RESET}")

    except ValueError:
        print(f"{YELLOW}Invalid input. Order cancelled.{RESET}")


def start(store):
    """Main function to start the user interface"""
    while True:
        display_menu()
        try:
            choice = input(f"{YELLOW}Enter your choice (1-4): {RESET}").strip()
            if choice not in ("1", "2", "3", "4"):
                raise ValueError

            if choice == '1':
                list_products(store)
            elif choice == '2':
                show_total_quantity(store)
            elif choice == '3':
                make_order(store)
            elif choice == '4':
                print_header("THANK YOU FOR SHOPPING WITH US")
                print(f"{YELLOW}Goodbye!{RESET}")
                sys.exit(0)
            else:
                print(f"{YELLOW}Invalid choice. Please enter a number between 1 and 4.{RESET}")
        except ValueError:
            print(f"{YELLOW}Invalid choice. Please enter a number between 1 and 4.{RESET}")

        input(f"\n{BLUE}Press Enter to continue...{RESET}")


def main():
    """ Initialises store and starts user interface """
    start(best_buy)


if __name__ == '__main__':
    main()
