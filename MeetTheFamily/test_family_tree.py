import pytest

def test_tree():
	print "df"
	raise ValueError("something is fishy")

# content of test_sample.py
def func(x):
    return x + 1

def test_answer():
    assert func(3) == 5