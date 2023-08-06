"""
McCalcy Calculator Module

This module provides a Calculator class for performing
basic arithmetic operations.
"""


class Calculator:
    """
    A simple calculator class that performs basic arithmetic operations.
    """

    def __init__(self) -> None:
        """
        Initializes a Calculator object with memory set to 0.
        """
        self.memory: float = 0

    def add(self, num: float) -> None:
        """
        Adds the given number to the memory.

        Args:
            num: The number to be added.

        Returns:
            None
        """
        try:
            self.memory += num
        except TypeError as exc:
            # Print an error message if value is not a number.
            raise TypeError(f"{num} is not a number") from exc

    def subtract(self, num: float) -> None:
        """
        Subtracts the given number from the memory.

        Args:
            num: The number to be subtracted.

        Returns:
            None
        """
        try:
            self.memory -= num
        except TypeError as exc:
            # Print an error message if value is not a number.
            raise TypeError(f"{num} is not a number") from exc

    def multiply(self, num: float) -> None:
        """
        Multiplies the memory by the given number.

        Args:
            num: The number to multiply by.

        Returns:
            None
        """

        try:
            self.memory *= num
        except TypeError as exc:
            # Print an error message if value is not a number.
            raise TypeError(f"{num} is not a number") from exc

    def divide(self, num: float) -> None:
        """
        Divides the memory by the given number.

        Args:
            num: The number to divide by.

        Returns:
            None
        """

        try:
            self.memory /= num
        except (TypeError, ZeroDivisionError) as exc:
            # Print an error message if wrong value.
            raise TypeError(f"Can't divide by {num}") from exc

    def root(self, root_value: int) -> None:
        """
        Calculates the nth root of a number.

        Args:
            root_value: The root value.

        Returns:
            None
        """

        try:
            root_value = float(root_value)
        except (TypeError, ValueError) as exc:
            raise TypeError(f"'{root_value}' is not a number") from exc

        if root_value < 1:
            raise ValueError("Root value must be greater than or equal to 1")

        try:
            result = self.memory ** (1 / root_value)
        except TypeError as exc:
            raise TypeError(f"'{self.memory}' is not a number") from exc

        self.memory = result

    def reset_memory(self) -> None:
        """
        Resets the memory to 0.

        Returns:
            None
        """
        self.memory = 0
