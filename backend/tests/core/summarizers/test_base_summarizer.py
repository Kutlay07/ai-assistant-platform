import pytest

from ai_assistant.core.summarizers import BaseSummarizer


def test_base_summarizer_cannot_be_instantiated():

    with pytest.raises(TypeError):
        BaseSummarizer()