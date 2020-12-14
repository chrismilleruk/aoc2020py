# Day 11: Seating System
import pytest
import time

# Simulate your seating area by applying the seating rules repeatedly until no seats change state. How many seats end up occupied?
def part1(data, directional = False):
  seating = Seating(data)
  step = 0
  for i in range(1000):
    step += 1
    start = time.perf_counter()
    changed = seating.step(directional)
    end = time.perf_counter()
    rtime = (end - start) * 1000 # sec -> ms
    print(f"Step {step} took {round(rtime)}ms - {seating.count_occupied()} occupied - changed:{changed}")
    if not changed: break
    
  return seating.count_occupied()

# Given the new visibility method and the rule change for occupied seats becoming empty, once equilibrium is reached, how many seats end up occupied?
def part2(data):
  return part1(data, True)


class Seating:
  def __init__(self, layout):
    self.frame = layout.split('\n')
    self.height = len(self.frame)
    self.width = len(self.frame[0])
    self.seats = [[x,y] for y, row in enumerate(self.frame) for x, seat in enumerate(row) if seat == 'L']
    self.adjacent = list(map(self.gen_adjacent, self.seats))
    self.directional = list(map(self.gen_directional, self.seats))

  def gen_adjacent(self, seat):
    [x, y] = seat
    x1, x2, y1, y2 = max(x-1, 0), min(x+2, self.width), max(y-1, 0), min(y+2, self.height)
    return [[x, y] for x in range(x1, x2) for y in range(y1, y2) if [x, y] != seat and self.frame[y][x] == 'L']

  def gen_directional(self, seat):
    [x, y] = seat
    rx = [list(range(x-1, -1, -1)), [x] * self.width, list(range(x+1, self.width, 1))]
    ry = [list(range(y-1, -1, -1)), [y] * self.height, list(range(y+1, self.height, 1))]

    lines_of_sight = [list(zip(dx, dy)) for dx in rx for dy in ry if not (dx == rx[1] and dy == ry[1])]
    # print(seat, lines_of_sight)
    # print(self.viz_lines(lines_of_sight))
    assert len(lines_of_sight) == 8

    seats = []
    for line in lines_of_sight:
      for [x, y] in line:
        if self.frame[y][x] == 'L':
          seats.append([x, y])
          break

    return seats

  def viz_lines(self, lines):
    frame = [list('.' * self.width) for _ in range(self.height)]
    for line in lines:
      for [x, y] in line:
        frame[y][x] = '+'
    return "\n".join(["".join(line) for line in frame])

  def count_occupied(self, seats = None):
    return list(map(lambda seat: self.frame[seat[1]][seat[0]], seats or self.seats)).count('#')
  
  def step(self, directional = False):
    changes_made = False
    tolerance = 5 if directional else 4
    next_frame = [list('.' * self.width) for _ in range(self.height)]
    for ([x, y], adjacent) in zip(self.seats, self.directional if directional else self.adjacent):
      occupied = self.count_occupied(adjacent)
      # If a seat is empty (L) and there are no occupied seats adjacent to it, the seat becomes occupied.
      if self.frame[y][x] == 'L' and occupied == 0:
        next_frame[y][x] = '#'
        changes_made = True
      # If a seat is occupied (#) and four or more seats adjacent to it are also occupied, the seat becomes empty.
      elif self.frame[y][x] == '#' and occupied >= tolerance:
        next_frame[y][x] = 'L'
        changes_made = True
      # Otherwise, the seat's state does not change.
      else:
        next_frame[y][x] = self.frame[y][x]
      # print(x, y, self.frame[y][x], "".join(map(lambda seat: self.frame[seat[1]][seat[0]], adjacent)), occupied, next_frame[y][x])
    self.frame = ["".join(line) for line in next_frame]
    return changes_made



# At this point, something interesting happens: the chaos stabilizes and further applications of these rules cause no seats to change state! Once people stop moving around, you count 37 occupied seats.
def test_part1(example1):
  assert part1(example1) == 37

def test_seating_step(example1):
  seating = Seating(example1)
  assert seating.frame == example1.split('\n')
  seating.step()
  assert seating.frame == """#.##.##.##
#######.##
#.#.#..#..
####.##.##
#.##.##.##
#.#####.##
..#.#.....
##########
#.######.#
#.#####.##""".split('\n')
  seating.step()
  assert seating.frame == """#.LL.L#.##
#LLLLLL.L#
L.L.L..L..
#LLL.LL.L#
#.LL.LL.LL
#.LLLL#.##
..L.L.....
#LLLLLLLL#
#.LLLLLL.L
#.#LLLL.##""".split('\n')
  seating.step()
  assert seating.frame == """#.##.L#.##
#L###LL.L#
L.#.#..#..
#L##.##.L#
#.##.LL.LL
#.###L#.##
..#.#.....
#L######L#
#.LL###L.L
#.#L###.##""".split('\n')
  seating.step()
  assert seating.frame == """#.#L.L#.##
#LLL#LL.L#
L.L.L..#..
#LLL.##.L#
#.LL.LL.LL
#.LL#L#.##
..L.L.....
#L#LLLL#L#
#.LLLLLL.L
#.#L#L#.##""".split('\n')
  seating.step()
  assert seating.frame == """#.#L.L#.##
#LLL#LL.L#
L.#.L..#..
#L##.##.L#
#.#L.LL.LL
#.#L#L#.##
..L.L.....
#L#L##L#L#
#.LLLLLL.L
#.#L#L#.##""".split('\n')

def test_seating_gen_directional(example1):
  seating = Seating(example1)
  assert seating.gen_directional([0,0]) == [[0,1], [2,0], [1,1]]
  assert seating.gen_directional([6,0]) == [[5,0], [5,1], [6, 1], [8,0], [9,3]]

def _test_seating_step2(example1):
  seating = Seating(example1)
  assert seating.frame == example1.split('\n')
  seating.step(True)
  assert seating.frame == """#.##.##.##
#######.##
#.#.#..#..
####.##.##
#.##.##.##
#.#####.##
..#.#.....
##########
#.######.#
#.#####.##""".split('\n')
  seating.step(True)
  assert seating.frame == """#.LL.LL.L#
#LLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLL#
#.LLLLLL.L
#.LLLLL.L#""".split('\n')
  seating.step(True)
  assert seating.frame == """#.L#.##.L#
#L#####.LL
L.#.#..#..
##L#.##.##
#.##.#L.##
#.#####.#L
..#.#.....
LLL####LL#
#.L#####.L
#.L####.L#""".split('\n')
  seating.step(True)
  assert seating.frame == """#.L#.L#.L#
#LLLLLL.LL
L.L.L..#..
##LL.LL.L#
L.LL.LL.L#
#.LLLLL.LL
..L.L.....
LLLLLLLLL#
#.LLLLL#.L
#.L#LL#.L#""".split('\n')
  seating.step(True)
  assert seating.frame == """#.L#.L#.L#
#LLLLLL.LL
L.L.L..#..
##L#.#L.L#
L.L#.#L.L#
#.L####.LL
..#.#.....
LLL###LLL#
#.LLLLL#.L
#.L#LL#.L#""".split('\n')
  seating.step(True)
  assert seating.frame == """#.L#.L#.L#
#LLLLLL.LL
L.L.L..#..
##L#.#L.L#
L.L#.LL.L#
#.LLLL#.LL
..#.L.....
LLL###LLL#
#.LLLLL#.L
#.L#LL#.L#""".split('\n')




@pytest.fixture
def example1():
  return """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL"""


