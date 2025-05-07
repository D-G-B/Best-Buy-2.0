class Product:
    """
    A class representing a product in an inventory system.
    """

    def __init__(self, name: str, price: float, quantity: int):
        """
        Initializes a Product instance.

        :param name: Name of the product.
        :param price: Price per unit of the product.
        :param quantity: Available quantity of the product.
        :raises ValueError: If name is empty or price/quantity is invalid.
        """
        if not name:
            raise ValueError("Name cannot be empty")

        self.name = name
        self.price = self._validate_non_negative_float(price, "Price")
        self.quantity = self._validate_non_negative_int(quantity, "Quantity")
        self.active = True

    @staticmethod
    def _validate_non_negative_float(value: float, field_name: str) -> float:
        """
        Validates that a given float value is non-negative.

        :param value: The float value to validate.
        :param field_name: Name of the field for error messages.
        :return: The validated non-negative float value.
        :raises ValueError: If the value is negative or not a number.
        """
        if not isinstance(value, (float, int)):
            raise ValueError(f"{field_name} must be a number.")
        if value < 0:
            raise ValueError(f"{field_name} cannot be negative.")
        return float(value)

    @staticmethod
    def _validate_non_negative_int(value: int, field_name: str) -> int:
        """
        Validates that a given int value is non-negative.

        :param value: The int value to validate.
        :param field_name: Name of the field for error messages.
        :return: The validated non-negative int value.
        :raises ValueError: If the value is not a non-negative integer.
        """
        if not isinstance(value, int):
            raise ValueError(f"{field_name} must be an integer.")
        if value < 0:
            raise ValueError(f"{field_name} cannot be negative.")
        return value

    @staticmethod
    def _validate_int(value: int, field_name: str) -> int:
        """
        Validates that a value is an integer.

        :param value: The value to validate.
        :param field_name: Name of the field for error messages.
        :return: The validated integer value.
        :raises ValueError: If the value is not an integer.
        """
        if not isinstance(value, int):
            raise ValueError(f"{field_name} must be an integer.")
        return value

    def get_quantity(self) -> int:
        """
        Returns the current quantity of the product.

        :return: The quantity of the product.
        """
        return self.quantity

    def set_quantity(self, quantity: int) -> None:
        """
        Sets the product's quantity, ensuring it is non-negative.
        Deactivates the product if the quantity becomes zero.

        :param quantity: The new quantity to set.
        :raises ValueError: If the quantity is negative.
        """
        self.quantity = self._validate_non_negative_int(quantity, "Quantity")
        if self.quantity == 0:
            self.active = False

    def is_active(self) -> bool:
        """
        Checks whether the product is active (in stock).

        :return: True if the product is active, False otherwise.
        """
        return self.active

    def activate(self) -> None:
        """
        Activates the product, making it available for purchase.
        """
        self.active = True

    def deactivate(self) -> None:
        """
        Deactivates the product, making it unavailable for purchase.
        """
        self.active = False

    def show(self) -> str:
        """
        Returns a string representation of the product.

        :return: A formatted string with product details.
        """
        return f"{self.name}, Price: {self.price}, Quantity: {self.quantity}"

    def buy(self, quantity: int) -> float:
        """
        Processes a purchase of the product, reducing stock accordingly.
        Deactivates the product if stock runs out.

        :param quantity: The quantity to purchase.
        :return: The total cost of the purchase.
        :raises ValueError: If the quantity to buy is negative or exceeds available stock.
        """
        quantity = self._validate_non_negative_int(quantity, "Quantity to buy")

        if quantity > self.quantity:
            raise ValueError("Not enough stock available. Try buying a smaller quantity")

        self.quantity -= quantity

        if self.quantity == 0:
            self.active = False

        return quantity * self.price


class NonStockedProduct(Product):
    """
    A class representing a non-physical product with no inventory (e.g., digital items).
    """

    def __init__(self, name: str, price: float):
        """
        Initializes a NonStockedProduct instance with quantity fixed to 0.

        :param name: Name of the product.
        :param price: Price of the product.
        """
        super().__init__(name, price, quantity=0)

    def set_quantity(self, quantity: int) -> None:
        """
        Raises an error when trying to set quantity for non-stocked products.

        :param quantity: Ignored.
        :raises Exception: Always, as quantity cannot be changed.
        """
        raise Exception("Non-stocked products are not physical and cannot have a quantity other than zero")

    def buy(self, quantity: int) -> float:
        """
        Processes purchase for a non-stocked product (always available).

        :param quantity: The number of units to "buy".
        :return: The total price.
        """
        quantity = self._validate_non_negative_int(quantity, "Quantity to buy")
        return quantity * self.price

    def show(self) -> str:
        """
        Returns a string representation for non-stocked products.

        :return: A formatted string indicating it is not stocked.
        """
        return f"{self.name}, Price: {self.price}, non-physical product - Not Stocked"


class LimitedProduct(Product):
    """
    A class representing a product with a maximum purchase limit per transaction.
    """

    def __init__(self, name: str, price: float, quantity: int, maximum: int):
        """
        Initializes a LimitedProduct instance.

        :param name: Name of the product.
        :param price: Price per unit.
        :param quantity: Available quantity.
        :param maximum: Maximum allowed quantity per purchase.
        """
        super().__init__(name, price, quantity)
        self.maximum = self._validate_non_negative_int(maximum, "Maximum quantity")

    def buy(self, quantity: int) -> float:
        """
        Processes a purchase, enforcing the maximum per-transaction limit.

        :param quantity: The quantity to buy.
        :return: The total price.
        :raises ValueError: If the quantity exceeds the maximum allowed.
        """
        if quantity > self.maximum:
            raise ValueError(f"Cannot purchase more than {self.maximum} units at a time.")
        return super().buy(quantity)

    def show(self) -> str:
        """
        Returns a string representation of the limited product.

        :return: A formatted string with price, quantity, and max purchase.
        """
        return f"{self.name}, Price: {self.price}, Quantity: {self.quantity}, Max Purchase: {self.maximum}"
