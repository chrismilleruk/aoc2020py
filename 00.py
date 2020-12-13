import pytest

def part1(data):
  return None

def part2(data):
  return None


def test_part1(example1):
  assert part1(example1) is None

@pytest.fixture
def example1():
  return """35
20
15"""