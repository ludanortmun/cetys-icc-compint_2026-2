import random

SEED = 42
ROLL = 6


def test_roll_d6_does_not_mutate_global_state_without_seed():
    old_state = random.getstate()
    from diceroll import dice
    _ = dice.roll_d6()
    assert random.getstate() == old_state, "Global random state was mutated"


def test_roll_d6_does_not_mutate_global_state_with_seed():
    old_state = random.getstate()
    from diceroll import dice
    _ = dice.roll_d6(seed=SEED)
    assert random.getstate() == old_state, "Global random state was mutated even with seed"


def test_roll_d6():
    from diceroll import dice
    result = dice.roll_d6()
    assert 1 <= result <= 6, "Dice roll is out of expected range"


def test_roll_d6_dice_roll_changes_on_subsequent_calls():
    results = set()
    for i in range(10):
        from diceroll import dice
        results.add(dice.roll_d6())
    assert len(results) > 1, "Dice roll did not change on subsequent calls"


def test_roll_d6_dice_roll_with_seed():
    from diceroll import dice
    result = dice.roll_d6(seed=SEED)
    assert 1 <= result <= 6, "Dice roll with seed is out of expected range"
    assert result == ROLL, "Dice roll with seed did not produce the expected result"
