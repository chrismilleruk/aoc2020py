# Day 5: Binary Boarding

# As a sanity check, look through your list of boarding passes. 
# What is the highest seat ID on a boarding pass?
def part1(data):
  return max(map(lambda x: decode_pass(x)['seat'], data.split('\n')))

def decode_pass(data):
  row = int("".join(str(['F', 'B'].index(ch)) for ch in data[0:7]), 2)
  col = int("".join(str(['L', 'R'].index(ch)) for ch in data[7:10]), 2)
  return {'row': row, 'column': col, 'seat': row * 8 + col}

def test_decode_pass(fn = decode_pass):
  # So, decoding FBFBBFFRLR reveals that it is the seat at row 44, column 5.
  # Every seat also has a unique seat ID: multiply the row by 8, then add the column. In this example, the seat has ID 44 * 8 + 5 = 357.
  tests = {
    'FBFBBFFRLR': { 'row': 44, 'column': 5, 'seat': 357 },
    'BFFFBBFRRR': { 'row': 70, 'column': 7, 'seat': 567 },
    'FFFBBBFRRR': { 'row': 14, 'column': 7, 'seat': 119 },
    'BBFFBBFRLL': { 'row': 102, 'column': 4, 'seat': 820 }
  }
  for test, expected in tests.items():
    assert fn(test) == expected


def part2(data):
  part2_test(part2_fn)
  print('self-check tests PASS')
  return part2_fn(data)

def part2_fn(data):
  return None

def part2_test(data):
  return None
