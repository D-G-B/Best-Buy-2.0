from abc import ABC, abstractmethod

class Promotion(ABC):
    """
    An abstract base class for defining product promotions.
    """
    def __init__(self, name: str):
        """
        Initializes a Promotion instance.

        :param name: The name of the promotion.
        """
        self.name = name

    @abstractmethod
    def apply_promotion(self, product, quantity: int) -> float:
        """
        Applies the promotion to a product for a given quantity.

        :param product: The Product instance.
        :param quantity: The quantity being purchased.
        :return: The discounted price after applying the promotion.
        """
        pass

class PercentDiscount(Promotion):
    """
    A promotion that applies a percentage discount to a product.
    """
    def __init__(self, name: str, percent: float):
        """
        Initializes a PercentDiscount promotion.

        :param name: The name of the promotion.
        :param percent: The discount percentage (e.g., 20 for 20%).
        :raises ValueError: If the percentage is not a non-negative number.
        """
        super().__init__(name)
        if not isinstance(percent, (int, float)) or percent < 0:
            raise ValueError("Discount percentage must be a non-negative number.")
        self.percent = percent / 100.0

    def apply_promotion(self, product, quantity: int) -> float:
        """
        Applies the percentage discount to the total price.

        :param product: The Product instance.
        :param quantity: The quantity being purchased.
        :return: The discounted total price.
        """
        return product.price * quantity * (1 - self.percent)

class SecondHalfPrice(Promotion):
    """
    A promotion where every second item is half price.
    """
    def __init__(self, name: str):
        """
        Initializes a SecondHalfPrice promotion.

        :param name: The name of the promotion.
        """
        super().__init__(name)

    def apply_promotion(self, product, quantity: int) -> float:
        """
        Applies the 'second item at half price' promotion.

        :param product: The Product instance.
        :param quantity: The quantity being purchased.
        :return: The discounted total price.
        """
        full_price_items = quantity // 2 + quantity % 2
        half_price_items = quantity // 2
        return (full_price_items * product.price) + (half_price_items * product.price * 0.5)

class ThirdOneFree(Promotion):
    """
    A promotion where every third item is free (buy 2, get 1 free).
    """
    def __init__(self, name: str):
        """
        Initializes a ThirdOneFree promotion.

        :param name: The name of the promotion.
        """
        super().__init__(name)

    def apply_promotion(self, product, quantity: int) -> float:
        """
        Applies the 'buy 2, get 1 free' promotion.

        :param product: The Product instance.
        :param quantity: The quantity being purchased.
        :return: The discounted total price.
        """
        free_items = quantity // 3
        paid_items = quantity - free_items
        return paid_items * product.price

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
        self._promotion = None  # Instance variable to hold the promotion

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

    def get_promotion(self) -> Promotion | None:
        """
        Returns the current promotion applied to the product.

        :return: The Promotion instance or None if no promotion is applied.
        """
        return self._promotion

    def set_promotion(self, promotion: Promotion) -> None:
        """
        Sets the promotion for the product.

        :param promotion: The Promotion instance to apply.
        """
        if isinstance(promotion, Promotion):
            self._promotion = promotion
        else:
            raise TypeError("Promotion must be an instance of the Promotion class or its subclasses.")

    def show(self) -> str:
        """
        Returns a string representation of the product, including the current promotion.

        :return: A formatted string with product details and promotion.
        """
        promotion_info = f", Promotion: {self._promotion.name}" if self._promotion else ""
        return f"{self.name}, Price: {self.price}, Quantity: {self.quantity}{promotion_info}"

    def buy(self, quantity: int) -> float:
        """
        Processes a purchase of the product, reducing stock and applying any active promotion.
        Deactivates the product if stock runs out.

        :param quantity: The quantity to purchase.
        :return: The total cost of the purchase after applying the promotion.
        :raises ValueError: If the quantity to buy is negative or exceeds available stock.
        """
        quantity = self._validate_non_negative_int(quantity, "Quantity to buy")

        if quantity > self.quantity:
            raise ValueError("Not enough stock available. Try buying a smaller quantity")

        self.quantity -= quantity

        if self.quantity == 0:
            self.active = False

        if self._promotion:
            return self._promotion.apply_promotion(self, quantity)
        else:
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
        Processes purchase for a non-stocked product (always available), applying any active promotion.

        :param quantity: The number of units to "buy".
        :return: The total price after promotion.
        """
        quantity = self._validate_non_negative_int(quantity, "Quantity to buy")
        if self._promotion:
            return self._promotion.apply_promotion(self, quantity)
        else:
            return quantity * self.price

    def show(self) -> str:
        """
        Returns a string representation for non-stocked products, including the current promotion.

        :return: A formatted string indicating it is not stocked and the promotion.
        """
        promotion_info = f", Promotion: {self._promotion.name}" if self._promotion else ""
        return f"{self.name}, Price: {self.price}, non-physical product - Not Stocked{promotion_info}"


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
        Processes a purchase, enforcing the maximum per-transaction limit and applying any promotion.

        :param quantity: The quantity to buy.
        :return: The total price after promotion.
        :raises ValueError: If the quantity exceeds the maximum allowed.
        """
        if quantity > self.maximum:
            raise ValueError(f"Cannot purchase more than {self.maximum} units at a time.")
        if self._promotion:
            return self._promotion.apply_promotion(self, quantity)
        else:
            return super().buy(quantity)

    def show(self) -> str:
        """
        Returns a string representation of the limited product, including the current promotion.

        :return: A formatted string with price, quantity, max purchase, and promotion.
        """
        promotion_info = f", Promotion: {self._promotion.name}" if self._promotion else ""
        return f"{self.name}, Price: {self.price}, Quantity: {self.quantity}, Max Purchase: {self.maximum}{promotion_info}"
