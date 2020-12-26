# Day 23: Crab Cups
import pytest

# Using your labeling, simulate 100 moves. What are the labels on the cups after cup 1?
def part1(data, moves = 100):
  nums = list(map(int, data))
  max_num = max(nums)
  min_num = min(nums)

  # Each move, the crab does the following actions:
  for i in range(moves):
    # The crab picks up the three cups that are immediately clockwise of the current cup. They are removed from the circle; cup spacing is adjusted as necessary to maintain the circle.
    [current, n1, n2, n3, *others] = nums
    picked_up = [n1, n2, n3]
    # The crab selects a destination cup: the cup with a label equal to the current cup's label minus one. If this would select one of the cups that was just picked up, the crab will keep subtracting one until it finds a cup that wasn't just picked up. If at any point in this process the value goes below the lowest value on any cup's label, it wraps around to the highest value on any cup's label instead.
    dest = current - 1
    # print(current, picked_up, others, dest)
    while dest in picked_up or dest < min_num:
      dest = dest - 1 if dest > min_num else max_num
      # print(current, picked_up, others, dest)

    # The crab places the cups it just picked up so that they are immediately clockwise of the destination cup. They keep the same order as when they were picked up.
    others.append(current)
    dest_idx = others.index(dest) + 1

    # The crab selects a new current cup: the cup which is immediately clockwise of the current cup.
    nums = others[:dest_idx] + picked_up + others[dest_idx:]

  # Starting after the cup labeled 1, collect the other cups' labels clockwise into a single string with no extra characters;
  idx = nums.index(1)
  nums = nums[idx+1:] + nums[:idx]
  return "".join(map(str, nums))

def part2(data):
  return None


def test_part1(example1):
  # after 10 moves, the cups clockwise from 1 are labeled 9, 2, 6, 5, and so on, producing 92658374. 
  # If the crab were to complete all 100 moves, the order after cup 1 would be 67384529.
  assert part1(example1, 0) == '25467389' #'389125467'
  assert part1(example1, 1) == '54673289' #'289154673'
  assert part1(example1, 2) == '32546789' #'546789132'
  assert part1(example1, 10) == '92658374'
  assert part1(example1, 100) == '67384529'

@pytest.fixture
def example1():
  return "389125467"
