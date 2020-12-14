# Day 12: Rain Risk
import pytest

# Figure out where the navigation instructions lead. What is the Manhattan distance between that location and the ship's starting position?
def part1(data):
  pos = [0, 0]
  dir = ['E', 'S', 'W', 'N']
  for instruction in data.split('\n'):
    command = instruction[0]
    number = int(instruction[1:])
    
    if command == 'L' or command == 'R':
      turns = (number // 90) % 4

      if command == 'L': turns = 4 - turns
      dir = dir[turns:] + dir[:turns]
      # print(instruction, command, turns, pos, dir)
      continue

    if command == 'F':
      command = dir[0]
    
    if command == 'W' or command == 'S':
      number = -number 

    if command == 'E' or command == 'W':
      pos[0] += number 
    if command == 'N' or command == 'S':
      pos[1] += number 
    
    # print(instruction, command, number, pos, dir[0])

  return sum(map(abs, pos))


def test_part1(example1):
  assert part1(example1) == 25

@pytest.fixture
def example1():
  return """F10
N3
F7
R90
F11"""