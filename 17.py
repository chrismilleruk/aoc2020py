# Day 17: Conway Cubes
import numpy as np 
import pytest

def part1(data, cycles = 6):
  grid = parseGrid(data)

  for i in range(cycles):
    grid = cycle(grid)
    grid = trim(grid)
    # print(grid)

  return np.sum(grid)

# def part2(data):
#   grid = parseGrid(data, axis = 4)

#   for i in range(6):
#     grid = cycle(grid)
#     grid = trim(grid)

#   return np.sum(grid)


def cycle(grid):
  shape = grid.shape
  # shape2 = (shape[0]+2, shape[1]+2, shape[2]+2)
  shape2 = list(map(lambda x: x+2, shape))
  dtype = grid.dtype
  grid2 = np.zeros(shape2, dtype)

  for idx, _ in np.ndenumerate(grid2):
    # since we increased the size of the grid, we need to 
    # translate grid2 idx to grid1 coords
    # me = theoretical centre of the 9x9x9 grid
    # print(idx)
    me = tuple(map(lambda x: x-1, idx))
    # fr = (max(0, me[0]-1), max(0, me[1]-1), max(0, me[2]-1))
    # to = (min(shape[0], me[0]+2), min(shape[1], me[1]+2), min(shape[2], me[2]+2))
    fr = tuple(map(lambda x: max(0, x-1), me))
    to = tuple(map(lambda x: min(x[0], x[1]+2), zip(shape, me)))

    # find out if the cube is active
    in_bounds = all([(a >= 0) for a in me]) and all([(a < b) for a, b in zip(me, shape)]) 
    active = 1 if in_bounds and grid[me] == 1 else 0

    # get the 9x9x9 block
    search = grid[fr[0]:to[0],fr[1]:to[1],fr[2]:to[2]]
    size = np.size(search)
    total = np.sum(search)

    # print(idx, me, active, fr, to, total, '/', size)

    #     During a cycle, all cubes simultaneously change their state according to the following rules:
    # If a cube is active and exactly 2 or 3 of its neighbors are also active, the cube remains active. Otherwise, the cube becomes inactive.
    # nb. exactly 3 or 4 including the active cube.
    if active and (total < 3 or total > 4):
      active = 0
    # If a cube is inactive but exactly 3 of its neighbors are active, the cube becomes active. Otherwise, the cube remains inactive.
    elif not active and total == 3:
      active = 1

    grid2[idx] = active

  return grid2

def trim(grid):
  size = len(grid.shape)

  def trim_axis(idx):
    start, stop = -1, grid.shape[idx] + 1
    axis_slice = [slice(None)] * size
    
    # found = 0
    # while not found:
    #   start += 1
    #   axis_slice[idx] = start
    #   found = np.any(grid[tuple(axis_slice)])

    # found = 0  
    # while not found:
    #   stop -= 1
    #   axis_slice[idx] = stop - 1
    #   found = np.any(grid[tuple(axis_slice)])

  
    for n in range(grid.shape[idx]):
      axis_slice[idx] = start = n
      if np.any(grid[tuple(axis_slice)]): break

    for n in range(grid.shape[idx], -1, -1):
      stop = n
      axis_slice[idx] = stop - 1
      if np.any(grid[tuple(axis_slice)]): break

    assert start < stop

    return slice(start, stop)

  slices = list(map(trim_axis, range(size)))
  # print(slices)
  
  return grid[tuple(slices)]

def parseGrid(data, axis = 3):
  if "z=" not in data:
    data = "z=0\n" + data
  xlam = lambda x: 1 if x == '#' else 0
  ylam = lambda y: list(map(xlam, y))
  zlam = lambda z: list(map(ylam, z.split('\n')[1:]))
  x1 = list(map(zlam, data.split('\n\n')))
  grid = np.array(x1, ndmin = axis)
  print(grid)
  return grid

def test_parseGrid(example1_cycles):
  # Before any cycles:
  np.testing.assert_equal(parseGrid(example1_cycles[0]), [[
    [0, 1, 0],
    [0, 0, 1],
    [1, 1, 1],
  ]])

  # After 1 cycle:
  example1_cycle1 = parseGrid(example1_cycles[1])
  np.testing.assert_array_equal(example1_cycle1, [[
    [1, 0, 0],
    [0, 0, 1],
    [0, 1, 0],
  ],[
    [1, 0, 1],
    [0, 1, 1],
    [0, 1, 0],
  ],[
    [1, 0, 0],
    [0, 0, 1],
    [0, 1, 0],
  ]])

def test_numpy_subset(example1_cycles):
  example1_cycle1 = parseGrid(example1_cycles[1])
  # Referencing a 3d subset
  np.testing.assert_array_equal(example1_cycle1[0:2,0:2,0:2], [[
    [1, 0],
    [0, 0],
  ],[
    [1, 0],
    [0, 1],
  ]])
  np.testing.assert_array_equal(example1_cycle1[1:3,1:3,1:3], [[
    [1, 1],
    [1, 0],
  ],[
    [0, 1],
    [1, 0],
  ]])

  # Counting 1s in a 3d subset
  assert np.sum(example1_cycle1[0:2,0:2,0:2]) == 3
  assert np.sum(example1_cycle1[1:3,1:3,1:3]) == 5
  
  # Counting out of range (above)
  assert np.sum(example1_cycle1[1:40,1:40,1:40]) == 5
  # Counting out of range (below) - '-1' means one from the end so this doesn't work
  # assert np.sum(example1_cycle1[-1:2,-1:2,-1:2]) == 3

def test_cycle_trim(example1_cycles):
  grid = parseGrid(example1_cycles[0])

  grid = trim(cycle(grid))
  example1_cycle = parseGrid(example1_cycles[1])
  np.testing.assert_array_equal(grid, example1_cycle)

  grid = trim(cycle(grid))
  example1_cycle = parseGrid(example1_cycles[2])
  np.testing.assert_array_equal(grid, example1_cycle)

  grid = trim(cycle(grid))
  example1_cycle = parseGrid(example1_cycles[3])
  np.testing.assert_array_equal(grid, example1_cycle)

# def test_cycle_trim_4d(example2_cycles):
#   grid = parseGrid(example2_cycles[0], axis = 4)

#   grid = trim(cycle(grid))
#   example2_cycle = parseGrid(example2_cycles[1])
#   np.testing.assert_array_equal(grid, example2_cycle)


# After the full six-cycle boot process completes, 112 cubes are left in the active state.
def test_part1(example1):
  assert part1(example1) == 112

# # After the full six-cycle boot process completes, 848 cubes are left in the active state.
# def test_part2(example1):
#   assert part2(example1) == 848

@pytest.fixture
def example1(example1_cycles):
  return example1_cycles[0]

@pytest.fixture
def example1_cycles():
  return [
# Before any cycles:
"""z=0
.#.
..#
###""",

# After 1 cycle:
"""z=-1
#..
..#
.#.

z=0
#.#
.##
.#.

z=1
#..
..#
.#.""",

# After 2 cycles:
"""z=-2
.....
.....
..#..
.....
.....

z=-1
..#..
.#..#
....#
.#...
.....

z=0
##...
##...
#....
....#
.###.

z=1
..#..
.#..#
....#
.#...
.....

z=2
.....
.....
..#..
.....
.....""",

# After 3 cycles:
"""z=-2
.......
.......
..##...
..###..
.......
.......
.......

z=-1
..#....
...#...
#......
.....##
.#...#.
..#.#..
...#...

z=0
...#...
.......
#......
.......
.....##
.##.#..
...#...

z=1
..#....
...#...
#......
.....##
.#...#.
..#.#..
...#...

z=2
.......
.......
..##...
..###..
.......
.......
......."""]


@pytest.fixture
def example2_cycles():
  return [
# Before any cycles:
"""z=0, w=0
.#.
..#
###""",

# After 1 cycle:
"""z=-1, w=-1
#..
..#
.#.

z=0, w=-1
#..
..#
.#.

z=1, w=-1
#..
..#
.#.

z=-1, w=0
#..
..#
.#.

z=0, w=0
#.#
.##
.#.

z=1, w=0
#..
..#
.#.

z=-1, w=1
#..
..#
.#.

z=0, w=1
#..
..#
.#.

z=1, w=1
#..
..#
.#.""",

# After 2 cycles:
"""z=-2, w=-2
.....
.....
..#..
.....
.....

z=-1, w=-2
.....
.....
.....
.....
.....

z=0, w=-2
###..
##.##
#...#
.#..#
.###.

z=1, w=-2
.....
.....
.....
.....
.....

z=2, w=-2
.....
.....
..#..
.....
.....

z=-2, w=-1
.....
.....
.....
.....
.....

z=-1, w=-1
.....
.....
.....
.....
.....

z=0, w=-1
.....
.....
.....
.....
.....

z=1, w=-1
.....
.....
.....
.....
.....

z=2, w=-1
.....
.....
.....
.....
.....

z=-2, w=0
###..
##.##
#...#
.#..#
.###.

z=-1, w=0
.....
.....
.....
.....
.....

z=0, w=0
.....
.....
.....
.....
.....

z=1, w=0
.....
.....
.....
.....
.....

z=2, w=0
###..
##.##
#...#
.#..#
.###.

z=-2, w=1
.....
.....
.....
.....
.....

z=-1, w=1
.....
.....
.....
.....
.....

z=0, w=1
.....
.....
.....
.....
.....

z=1, w=1
.....
.....
.....
.....
.....

z=2, w=1
.....
.....
.....
.....
.....

z=-2, w=2
.....
.....
..#..
.....
.....

z=-1, w=2
.....
.....
.....
.....
.....

z=0, w=2
###..
##.##
#...#
.#..#
.###.

z=1, w=2
.....
.....
.....
.....
.....

z=2, w=2
.....
.....
..#..
.....
....."""]