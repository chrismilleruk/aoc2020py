# Day 11: Seating System
import pytest
import time

# Simulate your seating area by applying the seating rules repeatedly until no seats change state. How many seats end up occupied?
def part1(data):
  seating = Seating(data)
  step = 0
  for i in range(1000):
    step += 1
    start = time.perf_counter()
    changed = seating.step()
    end = time.perf_counter()
    rtime = (end - start) * 1000 # sec -> ms
    print(f"Step {step} took {round(rtime)}ms - {seating.count_occupied()} occupied - changed:{changed}")
    if not changed: break
    
  return seating.count_occupied()


# def part2(data):
#   return None


class Seating:
  def __init__(self, layout):
    self.frame = layout.split('\n')
    self.height = len(self.frame)
    self.width = len(self.frame[0])
    self.seats = [[x,y] for y, line in enumerate(self.frame) for x, seat in enumerate(line) if seat == 'L']

  def count_adjacent(self, x, y):
    x1, x2, y1, y2 = max(x-1, 0), min(x+2, self.width), max(y-1, 0), min(y+2, self.height)
    return sum([line[x1:x2].count('#') for line in self.frame[y1:y2]]) - (1 if self.frame[y][x] == '#' else 0)
  
  def count_occupied(self):
    return "".join(self.frame).count('#')

  def step(self):
    changes_made = False
    next_frame = [list('.' * self.width) for _ in range(self.height)]
    for [x, y] in self.seats:
      # If a seat is empty (L) and there are no occupied seats adjacent to it, the seat becomes occupied.
      if self.frame[y][x] == 'L' and self.count_adjacent(x, y) == 0:
        next_frame[y][x] = '#'
        changes_made = True
      # If a seat is occupied (#) and four or more seats adjacent to it are also occupied, the seat becomes empty.
      elif self.frame[y][x] == '#' and self.count_adjacent(x, y) >= 4:
        next_frame[y][x] = 'L'
        changes_made = True
      # Otherwise, the seat's state does not change.
      else:
        next_frame[y][x] = self.frame[y][x]
    self.frame = ["".join(line) for line in next_frame]
    return changes_made




# If a seat is empty (L) and there are no occupied seats adjacent to it, the seat becomes occupied.
# If a seat is occupied (#) and four or more seats adjacent to it are also occupied, the seat becomes empty.
# Otherwise, the seat's state does not change.

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


