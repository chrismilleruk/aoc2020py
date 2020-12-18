# Day 18: Operation Order
import pytest

# Evaluate the expression on each line of the homework; what is the sum of the resulting values?
def part1(data):
  return None

def part2(data):
  return None

def test_part1(example1):
  # For example, the steps to evaluate the expression 1 + 2 * 3 + 4 * 5 + 6 are as follows:

  # 1 + 2 * 3 + 4 * 5 + 6
  #   3   * 3 + 4 * 5 + 6
  #       9   + 4 * 5 + 6
  #          13   * 5 + 6
  #              65   + 6
  #                  71
  assert part1("1 + 2 * 3 + 4 * 5 + 6") == 71
  # Parentheses can override this order; for example, here is what happens if parentheses are added to form 1 + (2 * 3) + (4 * (5 + 6)):

  # 1 + (2 * 3) + (4 * (5 + 6))
  # 1 +    6    + (4 * (5 + 6))
  #      7      + (4 * (5 + 6))
  #      7      + (4 *   11   )
  #      7      +     44
  #             51
  assert part1("1 + (2 * 3) + (4 * (5 + 6))") == 51

  # Here are a few more examples:
  # 2 * 3 + (4 * 5) becomes 26.
  assert part1("2 * 3 + (4 * 5)") == 26
  # 5 + (8 * 3 + 9 + 3 * 4 * 3) becomes 437.
  assert part1("5 + (8 * 3 + 9 + 3 * 4 * 3)") == 437
  # 5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4)) becomes 12240.
  assert part1("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))") == 12240
  # ((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2 becomes 13632.
  assert part1("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2") == 13632

@pytest.fixture
def example1():
  return "1 + 2 * 3 + 4 * 5 + 6"
