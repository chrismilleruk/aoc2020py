# Day 10: Adapter Array
import pytest

# What is the number of 1-jolt differences multiplied by the number of 3-jolt differences?
def part1(data):
  diffs = get_diffs(data)
  return diffs.count(1) * diffs.count(3)

# What is the total number of distinct ways you can arrange the adapters to connect the charging outlet to your device?
def part2(data):
  diffs = get_diffs(data)
  
  # chains of ones can be rearranged with 2s and 3s 
  # find chains of '1' and count the length
  prev = 0
  chains = []
  for n in diffs:
    if n == 1:
      if prev == 1:
        chains[-1] += 1
      else:
        chains.append(1)
    prev = n
  
  # chain length -> possibilities
  # 1 = 1
  # 2 = 2  123,   13
  # 3 = 4  1234,  124, 134,  14
  # 4 = 7  12345, 1345, 1245, 1235, 125, 135, 145, 
  lookup = [0, 1, 2, 4, 7]
  ways = 1
  for n in chains:
    ways *= lookup[n] 
  return ways


def get_diffs(data):
  numbers = [int(n) for n in data.split('\n') if n != '']
  numbers.sort()

  prev = 0
  for i in range(len(numbers)):
    diff = numbers[i] - prev
    prev = numbers[i]
    numbers[i] = diff
  numbers.append(3)

  return numbers
  

def test_part1_example1(example1):
  assert part1(example1) is 7 * 5

def test_part1_example2(example2):
  assert part1(example2) is 22 * 10

def test_part2_example1(example1):
  assert part2(example1) == 8

def test_part2_example2(example2):
  assert part2(example2) == 19208


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