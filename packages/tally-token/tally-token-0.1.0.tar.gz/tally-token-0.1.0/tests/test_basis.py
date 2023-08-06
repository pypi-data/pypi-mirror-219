from tally_token import split_text, merge_text


def test_split_merge():
    """Test that split_text and merge_text are inverses."""
    clear_text = "Hello World!"
    token1, token2 = split_text(clear_text)
    assert clear_text == merge_text(token1, token2)
