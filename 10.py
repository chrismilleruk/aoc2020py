# Day 10: Adapter Array
import pytest

# What is the number of 1-jolt differences multiplied by the number of 3-jolt differences?
def part1(data):
  numbers = [int(n) for n in data.split('\n') if n != '']
  numbers.sort()

  for i in range(len(numbers) - 1):
    numbers[i] = numbers[i+1] - numbers[i]
  numbers.pop()
  
  # print(numbers.count(1), numbers.count(2), numbers.count(3))
  # print(numbers)

  return (numbers.count(1) + 1) * (numbers.count(3) + 1)

# def part2(data):
#   return None


def test_part1(example1, example2):
  assert part1(example1) is 7 * 5
  assert part1(example2) is 22 * 10

# In this example, when using every adapter, there are 7 differences of 1 jolt and 5 differences of 3 jolts.
@pytest.fixture
def example1():
  return """16
10
15
5
1
11
7
19
6
12
4"""

# In this larger example, in a chain that uses all of the adapters, there are 22 differences of 1 jolt and 10 differences of 3 jolts.
@pytest.fixture
def example2():
  return """28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3
"""