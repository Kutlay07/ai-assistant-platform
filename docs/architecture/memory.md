# Memory

## Overview

Memory is responsible for storing and retrieving conversation history independently from workflow logic.

Workflows communicate exclusively through the `BaseMemory` abstraction, allowing memory implementations to be replaced without affecting application behavior.

The assistant remains completely independent from the underlying storage mechanism.



## BaseMemory

`BaseMemory` defines the common interface implemented by all memory providers.

The interface consists of:

- `get_history()` — return the stored messages.
- `add_message(role, content)` — append a message.
- `replace_history(messages)` — replace the stored messages.
- `get_summary()` — return the stored conversation summary, if any.
- `save_summary(summary)` — persist a conversation summary.

Messages are plain dictionaries with `role` and `content` keys, where `role` is one of
`system`, `user`, `assistant`, or `tool`.

See [Memory Architecture](../diagrams/memory-architecture.md) for the diagram.



### Current Implementations

- `FileMemory` (wired into the running application)
- `RedisMemory`
- `MockMemory`
- `SummarizingMemory` (decorator around any of the above)



### MockMemory

`MockMemory` is a lightweight in-memory implementation intended for development and testing.

Characteristics:

- Stores messages only in memory.
- No persistence.
- Fast and deterministic.
- Ideal for unit tests.

Conversation history is discarded when the application stops.



### FileMemory

`FileMemory` provides persistent conversation storage using a JSON file.

Characteristics:

- Loads conversation history on startup.
- Saves every new message automatically.
- Persists across application restarts.
- Storage location is configurable through `MEMORY_PATH`.

Conversation history is stored as a JSON array of role-tagged messages.

Example:

```json
[
    { "role": "user", "content": "Hello, I'm Kutlay" },
    { "role": "assistant", "content": "Hello Kutlay!" }
]
```

A legacy flat array of strings is still readable and is migrated to the role-tagged format
on first load.

The summary is stored next to the history file, using the same name with a `_summary`
suffix (for example `conversation_summary.json`).

The storage location can be configured through:

```text
MEMORY_PATH=data/conversation.json
```



### RedisMemory

`RedisMemory` stores the conversation and its summary in Redis under configurable keys.

It is implemented and unit-tested, but the running application currently wires
`FileMemory`, so Redis is not part of the Docker Compose stack.



## SummarizingMemory

`SummarizingMemory` decorates another `BaseMemory` implementation and keeps the prompt
bounded as a conversation grows.

When the stored history exceeds `max_messages`:

1. The oldest messages beyond the threshold are passed to a `BaseSummarizer`
   (`LLMSummarizer` in production, `MockSummarizer` in tests) together with the previous
   summary.
2. The resulting summary is persisted through `save_summary()`.
3. The remaining recent messages replace the stored history.

Workflows consume the summary by passing `memory.get_summary()` into `PromptBuilder`
alongside the recent history, so older context survives in condensed form.



### Planned Implementations

Future memory providers may include:

- `SQLiteMemory`

These implementations will continue to expose the same `BaseMemory` interface.