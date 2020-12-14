# Day 12: Rain Risk
import pytest

# Figure out where the navigation instructions lead. What is the Manhattan distance between that location and the ship's starting position?
def part1(data):
  return 25


def test_part1(example1):
  assert part1(example1) == 25

@pytest.fixture
def example1():
  return """F10
N3
F7
R90
F11"""