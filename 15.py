# Day 15: Rambunctious Recitation
import pytest

def part1(data):
  starting_numbers = list(map(int, data.split(',')))
  mem = dict((j,i+1) for i,j in enumerate(starting_numbers[:-1]))
  prev_num = starting_numbers[-1]

  for turn in range(len(starting_numbers), 2020):
    if prev_num not in mem:
      # If that was the first time the number has been spoken, the current player says 0.
      next_num = 0
      print(turn, ":", prev_num, '\t', '#', len(mem), "=", next_num)
    else:
      # Otherwise, the number had been spoken before; the current player announces how many turns apart the number is from when it was previously spoken.
      next_num = turn - mem[prev_num]
      print(turn, ":", prev_num, '\t', turn, '-', mem[prev_num], "=", next_num)
    
    mem[prev_num] = turn
    prev_num = next_num
  return prev_num


def test_part1(example1):
  # Their question for you is: what will be the 2020th number spoken? In the example above, the 2020th number spoken will be 436.
  assert part1(example1) == 436
  # Here are a few more examples:

  # Given the starting numbers 1,3,2, the 2020th number spoken is 1.
  assert part1("1,3,2") == 1
  # Given the starting numbers 2,1,3, the 2020th number spoken is 10.
  assert part1("2,1,3") == 10
  # Given the starting numbers 1,2,3, the 2020th number spoken is 27.
  assert part1("1,2,3") == 27
  # Given the starting numbers 2,3,1, the 2020th number spoken is 78.
  assert part1("2,3,1") == 78
  # Given the starting numbers 3,2,1, the 2020th number spoken is 438.
  assert part1("3,2,1") == 438
  # Given the starting numbers 3,1,2, the 2020th number spoken is 1836.
  assert part1("3,1,2") == 1836

@pytest.fixture
def example1():
  return """0,3,6"""