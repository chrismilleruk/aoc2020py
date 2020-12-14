# Day 12: Rain Risk
import pytest

# Figure out where the navigation instructions lead. What is the Manhattan distance between that location and the ship's starting position?
def part1(data):
  pos = [0, 0]
  dir = ['E', 'S', 'W', 'N']
  for instruction in data.split('\n'):
    command = instruction[0]
    number = int(instruction[1:])
    
    # Action L means to turn left the given number of degrees.
    # Action R means to turn right the given number of degrees.
    if command == 'L' or command == 'R':
      turns = (number // 90) % 4

      if command == 'L': turns = 4 - turns
      dir = dir[turns:] + dir[:turns]
      # print(instruction, command, turns, pos, dir)
      continue

    # Action F means to move forward by the given value in the direction the ship is currently facing.
    if command == 'F':
      command = dir[0]
    
    # Action N means to move north by the given value.
    # Action S means to move south by the given value.
    # Action E means to move east by the given value.
    # Action W means to move west by the given value.
    if command == 'W' or command == 'S':
      number = -number 
    if command == 'E' or command == 'W':
      pos[0] += number 
    if command == 'N' or command == 'S':
      pos[1] += number 
    
    # print(instruction, command, number, pos, dir[0])

  return sum(map(abs, pos))



# Figure out where the navigation instructions actually lead. What is the Manhattan distance between that location and the ship's starting position?
def part2(data):
  pos = [0, 0]
  waypoint = [10, 1]
  for instruction in data.split('\n'):
    command = instruction[0]
    number = int(instruction[1:])
    
    # Action F means to move forward to the waypoint a number of times equal to the given value.
    if command == 'F':
      pos[0] += waypoint[0] * number
      pos[1] += waypoint[1] * number
      # print(instruction, command, number, pos, waypoint)
      continue

    # Action N means to move the waypoint north by the given value.
    # Action S means to move the waypoint south by the given value.
    # Action E means to move the waypoint east by the given value.
    # Action W means to move the waypoint west by the given value.
    if command == 'W' or command == 'S':
      number = -number 
    if command == 'E' or command == 'W':
      waypoint[0] += number 
    if command == 'N' or command == 'S':
      waypoint[1] += number 
    
    # Action L means to rotate the waypoint around the ship left (counter-clockwise) the given number of degrees.
    # Action R means to rotate the waypoint around the ship right (clockwise) the given number of degrees.
    # [2, 1] L -> [-1, 2] -> [-2, -1] -> [1, -2]
    # [2, 1] R -> [1, -2] -> [-2, -1] -> [-1, 2]
    if command == 'L' or command == 'R':
      turns = (number // 90) % 4
      if command == 'L': turns = 4 - turns

      for _ in range(turns):
        waypoint = [waypoint[1], -waypoint[0]]

    # print(instruction, command, number, pos, waypoint)

  return sum(map(abs, pos))


def test_part1(example1):
  assert part1(example1) == 25


def test_part2(example1):
  assert part2(example1) == 286

@pytest.fixture
def example1():
  return """F10
N3
F7
R90
F11"""