# Day 15: Rambunctious Recitation
import pytest

def part1(data):
  return 436


def test_part1(example1):
  # Their question for you is: what will be the 2020th number spoken? In the example above, the 2020th number spoken will be 436.
  assert part1(example1) == 436
# Here are a few more examples:

# Given the starting numbers 1,3,2, the 2020th number spoken is 1.
# Given the starting numbers 2,1,3, the 2020th number spoken is 10.
# Given the starting numbers 1,2,3, the 2020th number spoken is 27.
# Given the starting numbers 2,3,1, the 2020th number spoken is 78.
# Given the starting numbers 3,2,1, the 2020th number spoken is 438.
# Given the starting numbers 3,1,2, the 2020th number spoken is 1836.

@pytest.fixture
def example1():
  return """0,3,6"""