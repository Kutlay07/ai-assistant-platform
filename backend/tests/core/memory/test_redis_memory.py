import json
from unittest.mock import MagicMock

from ai_assistant.core.memory.redis_memory import RedisMemory


def test_add_message_stores_message():
    memory = RedisMemory(client=MagicMock())
    
    memory.client = MagicMock()

    memory.client.get.return_value = None

    memory.add_message(
        "user",
        "hello",
    )

    memory.client.set.assert_called_once_with(
        "conversation",
        json.dumps(
            [
                {
                    "role": "user",
                    "content": "hello",
                }
            ]
        ),
        ex=3600,
    )


def test_get_history_returns_messages():
    
    memory = RedisMemory(client=MagicMock())
    
    memory.client = MagicMock()

    messages = [
        {
            "role": "assistant",
            "content": "hi",
        }
    ]

    memory.client.get.return_value = json.dumps(messages)

    result = memory.get_history()

    assert result == messages


def test_get_history_returns_empty_when_missing():
    memory = RedisMemory(client=MagicMock())
    
    memory.client = MagicMock()

    memory.client.get.return_value = None

    result = memory.get_history()

    assert result == []


def test_save_summary_stores_summary():

    memory = RedisMemory(client=MagicMock())

    memory.client.set.return_value = True

    memory.save_summary(
        "User is learning AI engineering."
    )

    memory.client.set.assert_called_once_with(
        "conversation:summary",
        "User is learning AI engineering.",
        ex=3600,
    )


def test_get_summary_returns_summary():

    memory = RedisMemory(client=MagicMock())

    memory.client.get.return_value = (
        "User is learning AI engineering."
    )

    result = memory.get_summary()

    assert result == (
        "User is learning AI engineering."
    )


def test_get_summary_decodes_bytes():

    memory = RedisMemory(client=MagicMock())

    memory.client.get.return_value = (
        b"User is learning AI engineering."
    )

    result = memory.get_summary()

    assert result == (
        "User is learning AI engineering."
    )


def test_get_summary_returns_none_when_missing():

    memory = RedisMemory(client=MagicMock())

    memory.client.get.return_value = None

    result = memory.get_summary()

    assert result is None