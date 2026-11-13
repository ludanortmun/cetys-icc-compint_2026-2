from copy import deepcopy
from dataclasses import replace

from conftest import make_result


def test_system_history_and_current_labeled_passages(pipeline):
    pipeline.config = replace(pipeline.config, history_turns=1)
    pipeline.history = [
        {"role": "user", "content": "old question"},
        {"role": "assistant", "content": "old answer"},
        {"role": "user", "content": "recent question"},
        {"role": "assistant", "content": "recent answer"},
    ]
    results = [make_result("DOCUMENT EVIDENCE ONE", source="a.txt"),
               make_result("DOCUMENT EVIDENCE TWO", source="b.txt")]
    before_history, before_results = deepcopy(pipeline.history), deepcopy(results)
    messages = pipeline.build_messages("CURRENT QUESTION", results)
    assert [message["role"] for message in messages] == ["system", "user", "assistant", "user"]
    assert isinstance(messages[0]["content"], str) and messages[0]["content"].strip()
    assert messages[1:3] == before_history[-2:]
    current = messages[-1]["content"]
    assert "CURRENT QUESTION" in current
    for result in results:
        doc = result.document
        assert f"[{doc.metadata['chunk_id']}]" in current
        assert doc.metadata["source"] in current
        assert doc.page_content in current
        assert doc.page_content not in messages[0]["content"]
    assert pipeline.history == before_history and results == before_results
    messages[1]["content"] = "mutation of returned message"
    assert pipeline.history == before_history


def test_zero_history_and_old_passages_are_not_carried_forward(pipeline):
    pipeline.config = replace(pipeline.config, history_turns=0)
    pipeline.history = [{"role": "user", "content": "old question"},
                        {"role": "assistant", "content": "old answer"}]
    first = pipeline.build_messages("first", [make_result("OLD PASSAGE")])
    second = pipeline.build_messages("second", [make_result("NEW PASSAGE")])
    assert [message["role"] for message in second] == ["system", "user"]
    assert "NEW PASSAGE" in second[-1]["content"]
    assert "OLD PASSAGE" not in str(second)
    assert "old question" not in str(second)
    assert "NEW PASSAGE" not in str(first)
