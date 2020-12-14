# Day 13: Shuttle Search
import pytest
from operator import itemgetter
from functools import reduce


# What is the ID of the earliest bus you can take to the airport multiplied by the number of minutes you'll need to wait for that bus?
def part1(data):
  lines = data.split('\n')
  now = int(lines[0])
  buses = list(map(int, [x for x in lines[1].split(',') if x != 'x']))
  print(now, buses)
  wait_times = list(map(lambda x: x - (now % x), buses))
  best_bus_wait = min(wait_times)
  best_bus_id = buses[wait_times.index(best_bus_wait)]
  print(list(wait_times), best_bus_wait, best_bus_id)
  return best_bus_id * best_bus_wait

# What is the earliest timestamp such that all of the listed bus IDs depart at offsets matching their positions in the list?
def part2(data):
  lines = data.split('\n')
  return part2_search(lines[1])

def part2_search(data):
  buses = enumerate(map(lambda x: int(x) if x != 'x' else 1, [x for x in data.split(',')]))
  buses = list(map(lambda x: (- x[0], x[1]), buses))
  buses = sorted(filter(lambda x: x[1] > 1, buses), key=itemgetter(1))
  print(buses)

  final = reduce(reduce_offset_period, buses)
  return final[0]

def reduce_offset_period(item1, item2):
  a, period1 = item1
  b, period2 = item2

  while a - b != 0:
    diff = abs(a - b)
    if a < b:
      if diff > period1:
        a += diff // period1 * period1
      else:
        a += period1
    else:
      if diff > period2:
        b += diff // period2 * period2
      else:
        b += period2

  print(period1, period2, (a, period1 * period2))
  return (a, period1 * period2)

def test_reduce_offset_period():
  assert reduce_offset_period((0, 5), (0, 7)) == (0, 7 * 5)
  assert reduce_offset_period((0, 5), (-2, 7)) == (5, 7 * 5)
  assert reduce_offset_period((0, 5), (-4, 7)) == (10, 7 * 5)
  assert reduce_offset_period((10, 35), (0, 45)) == (45, 35 * 45)

# The earliest bus you could take is bus ID 59. It doesn't depart until timestamp 944, so you would need to wait 944 - 939 = 5 minutes before it departs. Multiplying the bus ID by the number of minutes you'd need to wait gives 295.
def test_part1(example1):
  assert part1(example1) == 295

# In this example, the earliest timestamp at which this occurs is 1068781:
def test_part2(example1):
  # assert part2(example1) == 1068781

  # Here are some other examples:
  # The earliest timestamp that matches the list 17,x,13,19 is 3417.
  assert part2_search("17,x,13,19") == 3417
  # 67,7,59,61 first occurs at timestamp 754018.
  assert part2_search("67,7,59,61") == 754018
  # 67,x,7,59,61 first occurs at timestamp 779210.
  assert part2_search("67,x,7,59,61") == 779210
  # 67,7,x,59,61 first occurs at timestamp 1261476.
  assert part2_search("67,7,x,59,61") == 1261476
  # 1789,37,47,1889 first occurs at timestamp 1202161486.
  assert part2_search("1789,37,47,1889") == 1202161486

@pytest.fixture
def example1():
  return """939
7,13,x,x,59,x,31,19"""