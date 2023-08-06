class Calculator:
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
        self.memory += num

    def subtract(self, num: float) -> None:
        """
        Subtracts the given number from the memory.

        Args:
            num: The number to be subtracted.

        Returns:
            None
        """
        self.memory -= num

    def multiply(self, num: float) -> None:
        """
        Multiplies the memory by the given number.

        Args:
            num: The number to multiply by.

        Returns:
            None
        """
        self.memory *= num

    def divide(self, num: float) -> None:
        """
        Divides the memory by the given number.

        Args:
            num: The number to divide by.

        Returns:
            None
        """
        self.memory /= num

    def root(self, n: float) -> None:
        """
        Calculates the nth root of the memory.

        Args:
            n: The root value.

        Returns:
            None
        """
        self.memory **= (1/n)

    def reset_memory(self) -> None:
        """
        Resets the memory to 0.

        Returns:
            None
        """
        self.memory = 0
