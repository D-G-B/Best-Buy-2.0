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
        :raises ValueError: If name is empty or price/quantity is negative.
        """
        if not name:
            raise ValueError("Name cannot be empty")

        self.name = name
        self.price = self._validate_non_negative(price, "Price")
        self.quantity = self._validate_non_negative(quantity, "Quantity")
        self.active = True

    @staticmethod
    def _validate_non_negative(value: float, field_name: str) -> float:
        """
        Validates that a given value is non-negative.

        :param value: The value to validate.
        :param field_name: Name of the field for error messages.
        :return: The validated non-negative value.
        :raises ValueError: If the value is negative.
        """
        if value < 0:
            raise ValueError(f"{field_name} cannot be negative")
        return value

    @staticmethod
    def _validate_int(value: int, field_name: str) -> float:
        """
        Validates that a given value is an integer.

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
        self.quantity = self._validate_non_negative(quantity, "Quantity")
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
        quantity = self._validate_non_negative(quantity, "Quantity to buy")

        if quantity > self.quantity:
            raise ValueError("Not enough stock available. Try buying a smaller quantity")

        self.quantity -= quantity

        if self.quantity == 0:
            self.active = False

        return quantity * self.price

class NonStockedProduct(Product):
    def __init__(self, name: str, price: float ):
        super().__init__(name, price, quantity=0)

    def set_quantity(self, quantity: int) -> None:
        raise Exception("Non-stocked products are not physical and cannot have a quantity other than zero")

    def buy(self, quantity: int) -> float:
        quantity = self._validate_non_negative(quantity, "Quantity to buy")
        return quantity * self.price

    def show(self) -> str:
        return f"{self.name}, Price:{self.price}, non-physical product - Not Stocked"