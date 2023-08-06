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
        except TypeError:
            # Print an error message if value is not a number.
            print(f"{num} is not a number")

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
        except TypeError:
            # Print an error message if value is not a number.
            print(f"{num} is not a number")

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
        except TypeError:
            # Print an error message if value is not a number.
            print(f"{num} is not a number")

    def divide(self, num: float) -> None:
        """
        Divides the memory by the given number.

        Args:
            num: The number to divide by.

        Returns:
            None
        """

        # Try to calculate the division.
        try:
            result = self.memory / num
        except ZeroDivisionError:
            # Print an error message if user tries to divide by zero.
            print("Can't divide by zero, please select different value")
        except TypeError:
            # Print an error message if value is not a number.
            print(f"{num} is not a number")
        else:
            self.memory = result

    def nth_root(self, root_value: int) -> float:
        """
        Calculates the nth root of a number.

        Args:
            root_value: The root value.

        Returns:
            The nth root of the number.
        """

        # Check if the root value is less than 1.
        if root_value < 1:
            # Print an error message if value provided is less than 1.
            print("n value can't be less than 1")
            return

        # Try to calculate the nth root of the number.
        try:
            result = self.memory ** (1 / root_value)
        except TypeError:
            # Print an error message if value is not a number.
            print(f"{root_value} is not a number")
        else:
            # Set the memory to the result.
            self.memory = result

    def reset_memory(self) -> None:
        """
        Resets the memory to 0.

        Returns:
            None
        """
        self.memory = 0
