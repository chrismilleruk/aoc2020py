# Starting at the top-left corner of your map and following a slope of right 3 and down 1, how many trees would you encounter?
def part1(data, right = 3, down = 1):
  lines = data.split('\n')
  treecount = 0
  position = 0
  # right 3 and down 1
  for lineId in range(0, len(lines), down):
    line = lines[lineId]
    if line[position] == '#': treecount += 1
    position += right
    if position >= len(line): position -= len(line)
  return treecount

# What do you get if you multiply together the number of trees encountered on each of the listed slopes?
def part2(data):
  import operator
  import functools

  # Right 1, down 1.
  # Right 3, down 1. (This is the slope you already checked.)
  # Right 5, down 1.
  # Right 7, down 1.
  # Right 1, down 2.
  slopes = [
    [1, 1],
    [3, 1],
    [5, 1],
    [7, 1],
    [1, 2]
  ]

  return functools.reduce(operator.mul, map(lambda x: part1(data, x[0], x[1]), slopes))
