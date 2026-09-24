import pytest

from textpipeline import StopwordRemover, Token


def test_remove_stopwords_filters_the_supplied_english_words():
    tokens = [Token("this"), Token("food"), Token("is"), Token("good")]
    remover = StopwordRemover()
    assert remover.display_name() == "stopword_remover"
    assert repr(remover) == "stopword_remover"
    assert remover(tokens) == [Token("food"), Token("good")]


@pytest.mark.parametrize("invalid_tokens", [None, "tokens"])
def test_stopword_remover_rejects_invalid_tokens(invalid_tokens):
    with pytest.raises(TypeError):
        StopwordRemover()(invalid_tokens)


def test_stopword_remover_returns_no_tokens_for_empty_input():
    assert StopwordRemover()([]) == []
