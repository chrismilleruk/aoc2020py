# Day 14: Docking Data
import pytest
import re

# Execute the initialization program. What is the sum of all values left in memory after it completes?
def part1(data):
  mem = {}
  and_mask = 0
  or_mask = 0
  for (mask, memid, value) in map(parse_line, data.split('\n')):
    # print(mask or memid, value)
    if mask is not None:
      (and_mask, or_mask) = parse_mask(mask)
    elif memid is not None and value is not None:
      v = int(value) & and_mask | or_mask
      mem[memid] = v

  # print(mem)
  return sum(mem.values())
  # your answer is too high / 11926135976179
  #                           11926135976176

def parse_line(line):
  match = re.match(r"mask = (?P<mask>[X01]+)|mem\[(?P<memid>\d+)\] = (?P<value>\d+)", line)
  return match.groups()

# 
def parse_mask(mask):
  # XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X <-- this input
  # 111111111111111111111111111111111101 <-- resulting 'AND' mask
  # 000000000000000000000000000001000000 <-- resulting 'OR' mask
  and_mask = (1 << len(mask)) - 1
  or_mask = 0

  for i, ch in enumerate(mask[::-1]):
    if ch == '0':
      and_mask &= ~(1 << i)
    if ch == '1':
      or_mask |= 1 << i
  
  # print(f'{and_mask:036b}')
  # print(f'{or_mask:036b}')
  return (and_mask, or_mask)

def test_parse_mask():
  assert parse_mask( "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X") == (
                    0b111111111111111111111111111111111101,
                    0b000000000000000000000000000001000000
  )

# To initialize your ferry's docking program, you need the sum of all values left in memory after the initialization program completes. (The entire 36-bit address space begins initialized to the value 0 at every address.) In the above example, only two values in memory are not zero - 101 (at address 7) and 64 (at address 8) - producing a sum of 165.
def test_part1(example1):
  assert part1(example1) == 165

@pytest.fixture
def example1():
  return """mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0"""