# Day 20: Jurassic Jigsaw
import pytest
import re
import numpy as np
import operator
import functools
import itertools
import math
import enum
  
# Assemble the tiles into an image. What do you get if you multiply together the IDs of the four corner tiles?
def part1(data):
  tiles = parse(data)
  edges = get_edges(tiles)

  # Sort the tiles by the number of matching edges.
  # Corners will have 2 matching edges.
  # Sides will have 3 matching edges.
  # Middle will have 4 matching edges.
  fn = lambda t: (t.tile_id, list(map(lambda y: edges[y], t.meta[0])))
  sorted_tiles = list(sorted(map(fn, tiles.values()), key = lambda kv: sum([len(x) for x in kv[1]])))

  # Product of the first four sorted tiles
  return functools.reduce(operator.mul, map(lambda t: t[0], sorted_tiles[:4]))

def part2(data):
  image = create_image(data)
  return None



class Tile:
  def __init__(self, data):
    (self.tile_id, self.meta, self.original_grid) = parse_tile_data(data)
    self.transforms = []
  def __repr__(self):
    return f"Tile({self.tile_id})"
  def __str__(self):
    return f"Tile({self.tile_id}, {self.meta})"
  def set_links(self, links):
    self.links = links
  def orient(self, top, left):
    transforms = orient_tile(self.meta, top, left)
    if len(transforms) > 0:
      self.transforms = transforms
    return len(transforms) > 0
  def grid(self):
    m = self.original_meta
    g = self.original_grid
    for t in self.transforms:
      m, g = transform(t, m, g)
    return g




def create_image(data):
  tiles = parse(data)
  edges = get_edges(tiles)

  def edges_except(tile_id):
    return lambda edge: list(filter(lambda n: n != tile_id, edges[edge]))

  fn_tile = lambda t: (t.tile_id, list(map(edges_except(t.tile_id), t.meta[0])))
  tile_links = list(map(fn_tile, tiles.values()))
  sorted_links = sorted(tile_links, key = lambda kv: sum([len(x) for x in kv[1]]))
  
  unused_links = dict(itertools.starmap(lambda k,v: (k, list(map(lambda e: e[0] if len(e) > 0 else None, v))),  sorted_links.copy()))
  print(unused_links)
  
  sqrt = int(math.sqrt(len(sorted_links)))
  assert sqrt * sqrt == len(sorted_links)

  layout = np.array([ [ None for _ in range(sqrt) ] for _ in range(sqrt) ], dtype = Tile, ndmin = 2)
  print(layout)

  for y in range(sqrt):
    for x in range(sqrt):

      if y == 0 and x == 0:
        matches = [k for k, e in unused_links.items() if e.count(None) >= 2]
      else:
        top, left = [None], [None]
        if y > 0 and isinstance(layout[y-1, x], Tile):
          top = [layout[y-1, x].tile_id, -layout[y-1, x].tile_id]
        if x > 0 and isinstance(layout[y, x-1], Tile):
          left = [layout[y, x-1].tile_id, -layout[y, x-1].tile_id]
        print(x, y, top, left)
        matches = [k for k, e in unused_links.items() if any(np.in1d(top, e)) and any(np.in1d(left, e))]
      assert len(matches) > 0
      key = matches[0]
      print('\t', matches, tiles[key], unused_links.pop(key))
      layout[y, x] = tiles[key]
  # For reference, the IDs of the above tiles are:

  # 1951    2311    3079
  # 2729    1427    2473
  # 2971    1489    1171
  print(layout)

  # image = nd.array(ndmin = 2)
  # for y in range(sqrt):
  #   for x in range(sqrt):
  #     np.append()
  return {}

def parse(data):
  tiles = data.split('\n\n')
  result = {}
  for tile_data in tiles:
    tile = Tile(tile_data)
    result[tile.tile_id] = tile
    # print(tile_id, meta)
    # (tile_id, meta, grid) = parse_tile_data(tile_data)
    # result[tile_id] = (meta, grid)
  return result

def parse_tile_data(tile_data):
    lines = tile_data.split('\n')
    header = re.match(r'Tile (\d+)\:', lines[0])
    tile_id = int(header.groups()[0])
    grid = parse_hash_grid(lines[1:])
    borders = (grid[0,:], grid[:,-1], grid[-1,:], grid[:,0])
    meta = (list(map(lambda x: sum(j<<i for i,j in enumerate(x)), borders)), 
      list(map(lambda x: sum(j<<i for i,j in enumerate(reversed(x))), borders)))
    return (tile_id, meta, grid[1:-1, 1:-1])

def parse_hash_grid(lines):
  xlam = lambda x: 1 if x == '#' else 0
  ylam = lambda y: list(map(xlam, y))
  return np.array(list(map(ylam, lines)))

def get_edges(tiles):
  # 2311: ( ([300, 616, 924, 318], [210, 89, 231, 498]), ... )
  edges = {}
  # for tile_id, (meta, _) in tiles.items():
  for tile in tiles.values():
    print(tile)
    tile_id, meta = tile.tile_id, tile.meta
    for grp_id, group in enumerate(meta):
      for checksum in group:
        if checksum not in edges:
          edges[checksum] = []
        edges[checksum].append(tile_id if grp_id == 0 else -tile_id)
  return edges

# Using enum class create enumerations
class Transform(enum.Enum):
   NOOP = 0
   Rot_R = 1
   Rot_L = 2
   Flip_H = 3
   Flip_V = 4

def transform(transform_type, meta, grid = None):
  # ( ([Top, Right, Bottom, Left], [Rev_Top, Rev_Right, Rev_Bottom, Rev_Left]), tile_array )
  tr = get_meta_transform_map(transform_type)
  meta = tuple([[meta[(t[0] + rev) % 2][t[1]] for idx, t in enumerate(tr)] for rev, block in enumerate(meta)])
  if grid == None:
    return meta

  if transform_type == Transform.Flip_V:
    grid = np.fliplr(grid)
  elif transform_type == Transform.Flip_H:
    grid = np.flipud(grid)
  elif transform_type == Transform.Rot_R:
    grid = np.rot90(grid)
  elif transform_type == Transform.Rot_L:
    grid = np.rot90(grid, k = -1)
  
  return meta, grid

def get_meta_transform_map(transform_type = Transform.NOOP):
  (same, rev) = (0,1)
  [T,R,B,L] = [0,1,2,3]
  noop = [(same, T), (same, R), (same, B), (same, L)]
  flip_h = [(same, B), (rev, R), (same, T), (rev, L)]
  flip_v = [(rev, T), (same, L), (rev, B), (same, R)]
  rot_r = [(same, L), (same, T), (same, R), (same, B)]
  rot_l = [(same, R), (same, B), (same, L), (same, T)]
  transforms = [noop, rot_r, rot_l, flip_h, flip_v]
  return transforms[transform_type.value]

def orient_tile(meta, top, left):
  transforms = []
  if top in meta[1]:
    fl_top = meta[1].index(top)
    t = Transform.Flip_H if fl_top % 2 else Transform.Flip_V
    transforms.append(t)
    meta = transform(t, meta)
  if left in meta[1]:
    fl_left = meta[1].index(left)
    t = Transform.Flip_H if fl_left % 2 else Transform.Flip_V
    transforms.append(t)
    meta = transform(t, meta)
  assert top in meta[0] and left in meta[0], f'Flip failed {meta[0]} {transforms}'

  if meta[0].index(top) == 3:
    rot = [Transform.Rot_R]
  else:
    rot = [Transform.Rot_L] * meta[0].index(top)
  for t in rot:
    transforms.append(t)
    meta = transform(t, meta)
  assert top == meta[0][0] and left == meta[0][3], f'Rotate failed {top} {left} {meta[0]} {transforms}'
  
  return transforms

def test_part1(example1):
  # If you do this with the assembled tiles from the example above, you get 1951 * 3079 * 2971 * 1171 = 20899048083289.
  assert part1(example1) == 20899048083289

def test_transform():
  meta = ([1, 2, 3, 4], [-1, -2, -3, -4])
  assert transform(Transform.NOOP, meta) == ([1, 2, 3, 4], [-1, -2, -3, -4])
  assert transform(Transform.Rot_R, meta) == ([4, 1, 2, 3], [-4, -1, -2, -3])
  assert transform(Transform.Rot_L, meta) == ([2, 3, 4, 1], [-2, -3, -4, -1])
  assert transform(Transform.Flip_V, meta) == ([-1, 4, -3, 2], [1, -4, 3, -2])
  assert transform(Transform.Flip_H, meta) == ([3, -2, 1, -4], [-3, 2, -1, 4])
  # assert 1 in meta[0]

def test_orient_tile():
  meta = ([1, 2, 3, 4], [-1, -2, -3, -4])
  assert orient_tile(meta, 1, 4) == []
  assert orient_tile(meta, 2, 1) == [Transform.Rot_L]
  assert orient_tile(meta, 3, 2) == [Transform.Rot_L, Transform.Rot_L]
  assert orient_tile(meta, 4, 3) == [Transform.Rot_R]
  assert orient_tile(meta, -1, 2) == [Transform.Flip_V]
  assert orient_tile(meta, 3, -4) == [Transform.Flip_H]
  assert orient_tile(meta, -2, 3) == [Transform.Flip_H, Transform.Rot_L]
  assert orient_tile(meta, -3, -2) == [Transform.Flip_V, Transform.Flip_H]
  assert orient_tile(meta, -1, -4) == [Transform.Flip_V, Transform.Flip_H, Transform.Rot_L, Transform.Rot_L]


def test_create_image(example1, example1_actual_image):
  np.testing.assert_array_equal(create_image(example1), parse_hash_grid(example1_actual_image))

def test_part2(example1):
  # Determine how rough the waters are in the sea monsters' habitat by counting the number of # that are not part of a sea monster. In the above example, the habitat's water roughness is 273.
  assert part2(example1) == 273

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

@pytest.fixture
def example1_actual_image():
  return """.#.#..#.##...#.##..#####
###....#.#....#..#......
##.##.###.#.#..######...
###.#####...#.#####.#..#
##.#....#.##.####...#.##
...########.#....#####.#
....#..#...##..#.#.###..
.####...#..#.....#......
#..#.##..#..###.#.##....
#.####..#.####.#.#.###..
###.#.#...#.######.#..##
#.####....##..########.#
##..##.#...#...#.#.#.#..
...#..#..#.#.##..###.###
.#.#....#.##.#...###.##.
###.#...#..#.##.######..
.#.#.###.##.##.#..#.##..
.####.###.#...###.#..#.#
..#.#..#..#.#.#.####.###
#..####...#.#.#.###.###.
#####..#####...###....##
#.##..#..#...#..####...#
.#.###..##..##..####.##.
...###...##...#...#..###"""