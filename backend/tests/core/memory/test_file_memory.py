from ai_assistant.core.memory import FileMemory


def test_new_file_returns_empty_history(tmp_path):
    path = tmp_path / "conversation.json"

    memory = FileMemory(path)

    assert memory.get_history() == []


def test_add_message(tmp_path):
    path = tmp_path / "conversation.json"

    memory = FileMemory(path)
    
    memory.add_message(
    "user",
    "Hello",
    )

    assert memory.get_history() == [
        {
            "role": "user",
            "content": "Hello",
        }
    ]


def test_history_persists_between_instances(tmp_path):
    path = tmp_path / "conversation.json"

    memory1 = FileMemory(path)

    memory1.add_message(
    "user",
    "Hello",
    )

    memory2 = FileMemory(path)

    assert memory2.get_history() == [
        {
            "role": "user",
            "content": "Hello",
        }
    ]


def test_multiple_messages(tmp_path):
    memory = FileMemory(tmp_path / "memory.json")

    memory.add_message("user", "Hello")
    memory.add_message("assistant", "Hi")
    memory.add_message("user", "How are you?")

    assert memory.get_history() == [
        {
            "role": "user",
            "content": "Hello",
        },
        {
            "role": "assistant",
            "content": "Hi",
        },
        {
            "role": "user",
            "content": "How are you?",
        },
    ]


def test_memory_preserves_roles(tmp_path):
    memory = FileMemory(tmp_path / "memory.json")

    memory.add_message("assistant", "Hello first")

    messages = memory.get_messages()

    assert messages == [
        {
            "role": "assistant",
            "content": "Hello first",
        }
    ]


def test_save_and_get_summary(tmp_path):
    memory = FileMemory(tmp_path / "memory.json")

    memory.save_summary(
        "User is learning AI engineering."
    )

    assert memory.get_summary() == (
        "User is learning AI engineering."
    )