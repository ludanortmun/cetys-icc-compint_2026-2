import pytest

from textpipeline import SpecialCharacterRemover


def test_remove_special_characters_replaces_noise_with_spaces():
    remover = SpecialCharacterRemover()
    assert remover.display_name() == "special_character_remover"
    assert repr(remover) == "special_character_remover"
    assert remover("good-food! 100%") == "good food      "


@pytest.mark.parametrize("invalid_text", [None, 42])
def test_special_character_remover_rejects_invalid_text(invalid_text):
    with pytest.raises(TypeError):
        SpecialCharacterRemover()(invalid_text)


def test_special_character_remover_keeps_empty_text_empty():
    assert SpecialCharacterRemover()("") == ""
