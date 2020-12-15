# Day 15: Rambunctious Recitation
import pytest

def part1(data, stopAfter = 2020):
  starting_numbers = list(map(int, data.split(',')))
  mem = dict((j,i+1) for i,j in enumerate(starting_numbers[:-1]))
  prev_num = starting_numbers[-1]

  for turn in range(len(starting_numbers), stopAfter):
    if prev_num not in mem:
      # If that was the first time the number has been spoken, the current player says 0.
      next_num = 0
      # print(turn, ":", prev_num, '\t', '#', len(mem), "=", next_num)
    else:
      # Otherwise, the number had been spoken before; the current player announces how many turns apart the number is from when it was previously spoken.
      next_num = turn - mem[prev_num]
      # print(turn, ":", prev_num, '\t', turn, '-', mem[prev_num], "=", next_num)
    
    mem[prev_num] = turn
    prev_num = next_num
  return prev_num

def part2(data):
  # 2020th number in 361ms (1ms without instrumentation)
  # 30000000th number := 82 minutes (14s without inst.)
  return part1(data, 30000000)

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

# @pytest.mark.execution_timeout(20)
# def test_part2_1():
#   # Given 0,3,6, the 30000000th number spoken is 175594.
#   assert part2("0,3,6") == 175594

# @pytest.mark.execution_timeout(20)
# def test_part2_2():
#   # Given 1,3,2, the 30000000th number spoken is 2578.
#   assert part1("1,3,2") == 2578

# @pytest.mark.execution_timeout(20)
# def test_part2_3():
#   # Given 2,1,3, the 30000000th number spoken is 3544142.
#   assert part1("2,1,3") == 3544142

# @pytest.mark.execution_timeout(20)
# def test_part2_4():
#   # Given 1,2,3, the 30000000th number spoken is 261214.
#   assert part1("1,2,3") == 261214

# @pytest.mark.execution_timeout(20)
# def test_part2_5():
#   # Given 2,3,1, the 30000000th number spoken is 6895259.
#   assert part1("2,3,1") == 6895259

# @pytest.mark.execution_timeout(20)
# def test_part2_6():
#   # Given 3,2,1, the 30000000th number spoken is 18.
#   assert part1("3,2,1") == 18

# @pytest.mark.execution_timeout(20)
# def test_part2_7():
#   # Given 3,1,2, the 30000000th number spoken is 362.
#   assert part1("3,1,2") == 362


@pytest.fixture
def example1():
  return """0,3,6"""