from textpipeline import Postprocessor, Preprocessor, TextPipeline, Token, Tokenizer


def test_pipeline_defaults_to_empty_phases_and_word_tokenizer():
    pipeline = TextPipeline()
    assert pipeline.preprocessors == []
    assert pipeline.postprocessors == []
    assert pipeline.tokenizer.display_name() == "word_tokenizer"
    assert repr(pipeline) == (
        "textpipeline: {steps: {pre: (), tokenizer: (word_tokenizer), "
        "post: ()}, vocab_size: 0}"
    )


def test_pipeline_runs_phases_in_order_for_one_document():
    calls: list[str] = []

    class TestPreprocessor(Preprocessor):
        def __call__(self, text: str) -> str:
            calls.append("pre")
            return text + "!"

        def display_name(self) -> str:
            return "test_preprocessor"

    class TestTokenizer(Tokenizer):
        def __call__(self, text: str) -> list[Token]:
            calls.append("tokenizer")
            return [Token(text)]

        def display_name(self) -> str:
            return "test_tokenizer"

    class TestPostprocessor(Postprocessor):
        def __call__(self, tokens: list[Token]) -> list[Token]:
            calls.append("post")
            return [Token(token.value + "?") for token in tokens]

        def display_name(self) -> str:
            return "test_postprocessor"

    pipeline = TextPipeline([TestPreprocessor()], TestTokenizer(), [TestPostprocessor()])
    assert repr(pipeline) == (
        "textpipeline: {steps: {pre: (test_preprocessor), tokenizer: "
        "(test_tokenizer), post: (test_postprocessor)}, vocab_size: 0}"
    )
    assert pipeline.process("review", update_vocab=True) == [Token("review!?")]
    assert calls == ["pre", "tokenizer", "post"]
    assert repr(Token("review!?")) == "review!?"
    assert repr(pipeline).endswith("vocab_size: 1}")
