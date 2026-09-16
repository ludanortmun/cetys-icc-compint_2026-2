import random

SEED = 42
FIRST_D6_ROLLS = [6, 1, 1, 6, 3, 2, 2, 2, 6, 1]
FIRST_D10_ROLLS = [2, 1, 5, 4, 4, 3, 2, 9, 2, 10]


def test_roll_does_not_mutate_global_state_without_seed():
    old_state = random.getstate()
    from diceroll import dice
    _ = dice.roll()
    assert random.getstate() == old_state, "Global random state was mutated"


def test_roll_does_not_mutate_global_state_with_seed():
    old_state = random.getstate()
    from diceroll import dice
    _ = dice.roll(seed=SEED)
    assert random.getstate() == old_state, "Global random state was mutated even with seed"


def test_roll_invalid_parameters():
    from diceroll import dice
    import pytest
    with pytest.raises(ValueError):
        dice.roll(d=1)
    with pytest.raises(ValueError):
        dice.roll(n=0)
    with pytest.raises(ValueError):
        dice.roll(d=1, n=0)


def test_roll_defaults_to_single_d6():
    from diceroll import dice
    result = dice.roll()
    assert 1 <= result <= 6, "Dice roll is out of expected range"


def test_roll_dice_roll_changes_on_subsequent_calls():
    results = set()
    for i in range(10):
        from diceroll import dice
        results.add(dice.roll())
    assert len(results) > 1, "Dice roll did not change on subsequent calls"


def test_roll_dice_roll_with_seed():
    from diceroll import dice
    result = dice.roll(seed=SEED)
    assert 1 <= result <= 6, "Dice roll with seed is out of expected range"
    assert result == 6, "Dice roll with seed did not produce the expected result"


def test_roll_multiple_dice_without_seed():
    from diceroll import dice
    result = dice.roll(d=6, n=10)
    assert 10 <= result <= 60, "Sum of multiple dice rolls is out of expected range"


def test_roll_multiple_dice_with_seed():
    from diceroll import dice
    result = dice.roll(d=6, n=10, seed=SEED)
    assert 10 <= result <= 60, "Sum of multiple dice rolls with seed is out of expected range"
    assert result == sum(
        FIRST_D6_ROLLS), "Sum of multiple dice rolls with seed did not produce the expected result"


def test_roll_multiple_d10_with_seed():
    from diceroll import dice
    result = dice.roll(d=10, n=10, seed=SEED)
    assert 10 <= result <= 100, "Sum of multiple D10 dice rolls with seed is out of expected range"
    assert result == sum(
        FIRST_D10_ROLLS), "Sum of multiple D10 dice rolls with seed did not produce the expected result"
