# Day 19: Monster Messages
import pytest

def part1(data):
  rules, messages = parse(data)
  print(rules, messages)
  return None

def parse(data):
  [rules, messages] = data.split('\n\n')
  rules = dict(map(lambda x: x.split(': '), rules.split('\n')))
  messages = messages.split('\n')
  return rules, messages

# In the above example, ababbb and abbbab match, but bababa, aaabbb, and aaaabbb do not, producing the answer 2.
def test_part1(example1):
  assert part1(example1) == 2

@pytest.fixture
def example1():
  return """0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb"""

@pytest.fixture
def example2():
  return """0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"
"""