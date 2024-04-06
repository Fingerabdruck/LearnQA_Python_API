import pytest

def test_phrase():
    phrase = input("Set a phrase: ")
    assert len(phrase) < 15, "Фраза должна быть короче 15 символов"
