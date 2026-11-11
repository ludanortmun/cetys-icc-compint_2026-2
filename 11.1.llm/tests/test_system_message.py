from chat.cli import SYSTEM_MESSAGE


def test_system_message_is_populated():
    assert isinstance(SYSTEM_MESSAGE, str) and SYSTEM_MESSAGE.strip()
