# Language Models

## Overview

Language models are responsible for generating responses from prompts.

The assistant communicates with language model providers exclusively through the `BaseLLM` abstraction, making the system provider-independent.

This allows providers to be replaced without changing workflow implementations.



## BaseLLM

`BaseLLM` defines the common interface implemented by every language model provider.

All providers expose the same contract while hiding provider-specific implementation details:

- `generate(prompt) -> str`
- `generate_with_tools(messages, tools) -> str | ToolCall`
- `stream(prompt) -> Iterator[str]`

Providers are constructed by the `create_llm()` factory, which selects an implementation
from the `LLM_PROVIDER` environment variable.

The assistant depends only on this abstraction.

See [Provider Independence](../diagrams/provider-independence.md) for the diagram.



### Current Implementations

- `GroqProvider`
- `MockLLM`
- `LocalProvider`



## GroqProvider

`GroqProvider` connects the assistant to Groq's OpenAI-compatible API.

Characteristics:

- Production-ready
- Supports text generation
- Supports streaming responses
- Compatible with OpenAI-style APIs



## MockLLM

`MockLLM` is a lightweight implementation intended for development and testing.

Characteristics:

- Deterministic responses
- No external dependencies
- Fast execution
- Ideal for unit tests



## LocalProvider

`LocalProvider` is a placeholder reserved for future support of locally hosted language
models. Every method currently raises `NotImplementedError`; selecting `LLM_PROVIDER=local`
will therefore fail at request time.

Potential future integrations include:

- Ollama
- vLLM
- llama.cpp
- Hugging Face Transformers

All local providers will continue to implement the `BaseLLM` interface.