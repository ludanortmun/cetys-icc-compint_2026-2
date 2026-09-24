import pytest

from textpipeline import CasingNormalizer


def test_normalize_casing_lowercases_text():
    normalizer = CasingNormalizer()
    assert normalizer.display_name() == "case_normalizer"
    assert repr(normalizer) == "case_normalizer"
    assert normalizer("Very GOOD!") == "very good!"


@pytest.mark.parametrize("invalid_text", [None, 42])
def test_casing_normalizer_rejects_invalid_text(invalid_text):
    with pytest.raises(TypeError):
        CasingNormalizer()(invalid_text)


def test_casing_normalizer_keeps_empty_text_empty():
    assert CasingNormalizer()("") == ""
