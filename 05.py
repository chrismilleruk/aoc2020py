# Day 5: Binary Boarding

# As a sanity check, look through your list of boarding passes. 
# What is the highest seat ID on a boarding pass?
def part1(data):
  return max(map(lambda x: decode_pass(x)['seat'], data.split('\n')))

# It's a completely full flight, so your seat should be the only missing boarding pass in your list. 
# Your seat wasn't at the very front or back, though; the seats with IDs +1 and -1 from yours will be in your list.
# What is the ID of your seat?
def part2(data):
  passes = list(map(lambda x: decode_pass(x)['seat'], data.split('\n')))
  seats = set(range(min(passes), max(passes)))
  missing = seats.difference(passes)
  return missing




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
