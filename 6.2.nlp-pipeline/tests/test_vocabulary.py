from textpipeline import TextPipeline, Token, Tokenizer


class SplitTokenizer(Tokenizer):
    def __call__(self, text: str) -> list[Token]:
        return [Token(token) for token in text.split()]

    def display_name(self) -> str:
        return "split_tokenizer"


class WholeDocumentTokenizer(Tokenizer):
    def __call__(self, text: str) -> list[Token]:
        return [Token(text)]

    def display_name(self) -> str:
        return "whole_document_tokenizer"


def test_pipeline_learns_unique_final_tokens_across_documents():
    pipeline = TextPipeline([], SplitTokenizer())
    pipeline.process("known known", update_vocab=True)
    pipeline.process("also-known", update_vocab=True)
    assert pipeline.vocabulary == {Token("known"), Token("also-known")}


def test_frozen_pipeline_replaces_unseen_final_tokens_without_mutating_vocabulary():
    pipeline = TextPipeline([], WholeDocumentTokenizer())
    pipeline.process("known", update_vocab=True)
    assert pipeline.process("new", update_vocab=False) == [Token("<unk>")]
    assert pipeline.vocabulary == {Token("known")}
