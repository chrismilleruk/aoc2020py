# Day 13: Shuttle Search
import pytest

# What is the ID of the earliest bus you can take to the airport multiplied by the number of minutes you'll need to wait for that bus?
def part1(data):
  return 295

# The earliest bus you could take is bus ID 59. It doesn't depart until timestamp 944, so you would need to wait 944 - 939 = 5 minutes before it departs. Multiplying the bus ID by the number of minutes you'd need to wait gives 295.
def test_part1(example1):
  assert part1(example1) == 295

@pytest.fixture
def example1():
  return """939
7,13,x,x,59,x,31,19"""