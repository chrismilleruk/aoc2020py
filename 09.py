# Day 9: Encoding Error
import pytest

# The first step of attacking the weakness in the XMAS data is to find the first number in the list (after the preamble) which is not the sum of two of the 25 numbers before it. What is the first number that does not have this property?
def part1(data, period = 25):
  return 127


# In this example, after the 5-number preamble, almost every number is the sum of two of the previous 5 numbers; the only number that does not follow this rule is 127.
def test_part1(example1):
  assert part1(example1, 5) == 127

@pytest.fixture
def example1():
  return """35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576
"""


