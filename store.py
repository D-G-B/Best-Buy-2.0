from products import Product


class Store:
    """
    A class representing a store that manages a collection of products.
    """

    def __init__(self, products: list[Product]):
        """
        Initializes the store with a list of products.

        :param products: A list of Product objects available in the store.
        """
        self.products = products

    def add_product(self, product: Product) -> None:
        """
        Adds a new product to the store's inventory.

        :param product: The Product object to add.
        """
        self.products.append(product)

    def remove_product(self, product: Product) -> None:
        """
        Removes a product from the store's inventory if it exists.

        :param product: The Product object to remove.
        """
        if product in self.products:
            self.products.remove(product)

    def get_total_quantity(self) -> int:
        """
        Calculates the total quantity of all products in the store.

        :return: The sum of all product quantities.
        """
        return sum(product.get_quantity() for product in self.products)

    def get_all_products(self) -> list[Product]:
        """
        Retrieves all active products in the store.

        :return: A list of active Product objects.
        """
        return [p for p in self.products if p.is_active()]

    @staticmethod
    def order(shopping_list: list[tuple[Product, int]]) -> float:
        """
        Processes an order by purchasing specified quantities of products.

        :param shopping_list: A list of tuples, where each tuple contains a
                                Product object and the quantity to buy.
        :return: The total cost of the order.
        """
        total_price = 0
        for product, quantity in shopping_list:
            total_price += product.buy(quantity)
        return total_price
