# Day 9: Encoding Error
import pytest

# The first step of attacking the weakness in the XMAS data is to find the first number in the list (after the preamble) which is not the sum of two of the 25 numbers before it. What is the first number that does not have this property?
def part1(data, period = 25):
  numbers = [int(n) for n in data.split('\n') if n != '']

  # store precacluated sums with the following 
  # array structure:
  #    a | b | c | d | e | f
  # a|[a,  ab, ac, ad, ae]
  # b|    [b,  bc, bd, be]+[bf]
  # c|        [c,  cd, ce]+[cf]
  # d|            [d,  de]+[df]
  # e|                [e] +[ef]
  # f|                     [f]
  sums = list(map(lambda x: [x], numbers[0:period]))
  for i in range(1, period):
    for j in range(i-1, -1, -1):
      sums[j].append(sums[j][0] + sums[i][0])
  # print(period, sums)

  for n in numbers[period:]:
    # validate n
    valid = False
    for sum in sums:
      if n in sum[1:]:
        valid = True
        break
    
    # return first number that does not validate
    if not valid:
      return n

    # update sums
    sums.append([n])
    for j in range(period-1, -1, -1):
      sums[j].append(sums[j][0] + n)
    sums = sums[1:]

  return None

# What is the encryption weakness in your XMAS-encrypted list of numbers?
def part2(data, target = 466456641):
  numbers = [int(n) for n in data.split('\n') if n != '']
  sums = numbers.copy()

  for i in range(len(sums)):
    for j in range(i -1, -1, -1):
      sums[j] += sums[i]
      if sums[j] == target:
        return min(numbers[j:i]) + max(numbers[j:i])
  

# In this example, after the 5-number preamble, almost every number is the sum of two of the previous 5 numbers; the only number that does not follow this rule is 127.
def test_part1(example1):
  assert part1(example1, 5) == 127

# To find the encryption weakness, add together the smallest and largest number in this contiguous range; in this example, these are 15 and 47, producing 62.
def test_part2(example1):
  assert part2(example1, 127) == 62

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


