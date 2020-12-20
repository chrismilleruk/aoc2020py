# Day 20: Jurassic Jigsaw
import pytest
import re
import numpy as np
import operator
import functools

# Assemble the tiles into an image. What do you get if you multiply together the IDs of the four corner tiles?
def part1(data):
  tiles = parse(data)
  edges = get_edges(tiles)

  # Sort the tiles by the number of matching edges.
  # Corners will have 2 matching edges.
  # Sides will have 3 matching edges.
  # Middle will have 4 matching edges.
  fn = lambda x: (x[0], sum(map(lambda y: len(edges[y]), x[1][0][0])))
  sorted_tiles = sorted(map(fn, tiles.items()), key = lambda kv: kv[1])

  # Product of the first four sorted tiles
  return functools.reduce(operator.mul, map(lambda t: t[0], sorted_tiles[:4]))

def part2(data):
  return None

def parse(data):
  tiles = data.split('\n\n')
  result = {}
  for tile_data in tiles:
    lines = tile_data.split('\n')
    header = re.match(r'Tile (\d+)\:', lines[0])
    tile_id = int(header.groups()[0])
    grid = parseTile(lines[1:])
    borders = (grid[0,:], grid[:,-1], grid[-1,:], grid[:,0])
    meta = (list(map(lambda x: sum(j<<i for i,j in enumerate(x)), borders)), 
      list(map(lambda x: sum(j<<i for i,j in enumerate(reversed(x))), borders)))
    # print(tile_id, meta)
    result[tile_id] = (meta, grid)
  return result

def parseTile(lines):
  xlam = lambda x: 1 if x == '#' else 0
  ylam = lambda y: list(map(xlam, y))
  return np.array(list(map(ylam, lines)))

def get_edges(tiles):
  # 2311: ( ([300, 616, 924, 318], [210, 89, 231, 498]), ... )
  edges = {}
  for tile_id, (meta, _) in tiles.items():
    for grp_id, group in enumerate(meta):
      for checksum in group:
        if checksum not in edges:
          edges[checksum] = []
        edges[checksum].append(tile_id if grp_id == 0 else -tile_id)
  return edges

def test_part1(example1):
  # If you do this with the assembled tiles from the example above, you get 1951 * 3079 * 2971 * 1171 = 20899048083289.
  assert part1(example1) == 20899048083289

@pytest.fixture
def example1():
  return """Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###..."""