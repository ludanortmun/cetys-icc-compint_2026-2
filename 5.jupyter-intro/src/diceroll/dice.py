from random import Random


def roll_d6(seed: int | None = None) -> int:
    """
    Roll a six-sided die (D6).

    Args:
        seed (int | None): Optional seed for the random number generator.

    Returns:
        int: Result of the dice roll (1-6).
    """
    raise NotImplementedError()


def roll(d: int = 6, n: int = 1, seed: int | None = None) -> int:
    """
    EXTRA CREDIT:
    Roll a dice with a specified number of sides multiple times. 
    All dice rolls use the same random number generator, optionally seeded with the provided `seed`.

    Args:
        d (int): Number of sides on the dice (default is 6).
        n (int): Number of times to roll the dice (default is 1).
        seed (int | None): Optional seed for the random number generator.

    Returns:
        int: Result of the dice roll. Sum of all `n` rolls.

    Raises:
        ValueError: If the number of sides `d` is less than 2, or the number of rolls `n` is less than 1.
    """
    raise NotImplementedError()
