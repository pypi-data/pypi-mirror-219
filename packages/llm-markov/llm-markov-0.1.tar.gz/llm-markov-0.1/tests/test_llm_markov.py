from click.testing import CliRunner
from llm.cli import cli
import pytest
import time


@pytest.mark.parametrize("length", [10, 20])
def test_markov_prompt(length):
    runner = CliRunner()
    prompt = "the quick brown fox jumped over the lazy dog"
    args = [
        prompt,
        "-m",
        "markov",
        "-o",
        "length",
        str(length),
    ]
    result = runner.invoke(cli, args)
    assert result.exit_code == 0, result.output
    words = result.output.strip().split()
    # ['lazy', 'dog', 'brown', 'fox', 'jumped', 'over', 'the', 'quick', 'brown']
    # Every word should be one of the original prompt
    prompt_words = prompt.split()
    for word in words:
        assert word in prompt_words
    assert len(words) == length
