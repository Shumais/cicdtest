# content of test_sample.py
def inc(x):
    return x + 1

def test_answer_wrong():
    assert inc(3) == 5
	
def test_answer_correct():
    assert inc(4) == 5