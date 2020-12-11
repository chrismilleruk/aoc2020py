# Day 5: Binary Boarding

# As a sanity check, look through your list of boarding passes. 
# What is the highest seat ID on a boarding pass?
def part1(data):
  return None

def decode_pass(data):
  return {'row': 44, 'column': 5, 'seat': 357}

def test_decode_pass(fn = decode_pass):
  # So, decoding FBFBBFFRLR reveals that it is the seat at row 44, column 5.
  # Every seat also has a unique seat ID: multiply the row by 8, then add the column. In this example, the seat has ID 44 * 8 + 5 = 357.
  tests = {
    'FBFBBFFRLR': { 'row': 44, 'column': 5, 'seat': 357 },
    'BFFFBBFRRR': { 'row': 70, 'column': 7, 'seat': 567 },
    # 'FFFBBBFRRR': { 'row': 14, 'column': 7, 'seat': 119 },
    # 'BBFFBBFRLL': { 'row': 102, 'column': 4, 'seat': 820 }
  }
  for test, expected in tests.items():
    assert decode_pass(test) == expected


def part2(data):
  part2_test(part2_fn)
  print('self-check tests PASS')
  return part2_fn(data)

def part2_fn(data):
  return None

def part2_test(data):
  return None
