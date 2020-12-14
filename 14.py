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
      (and_mask, or_mask, _) = parse_mask(mask)
    elif memid is not None and value is not None:
      v = int(value) & and_mask | or_mask
      mem[memid] = v

  # print(mem)
  return sum(mem.values())
  # your answer is too high / 11926135976179
  #                           11926135976176

def part2(data):
  mem = {}
  or_mask = 0
  float_mask = 0
  float_bits = []
  for (mask, memid, value) in map(parse_line, data.split('\n')):
    # print(mask or memid, value)
    if mask is not None:
      (_, or_mask, float_mask) = parse_mask(mask)
      float_bits = [i for i, ch in enumerate(bin(float_mask)[:1:-1]) if ch == '1']
    elif memid is not None and value is not None:
      v = int(value)
      
      # Floating bits take on every possible combination of values; with two floating bits, four actual memory addresses are written
      for n in range(1 << len(float_bits)):
        # It first applies the bitmask:
        memid2 = int(memid) | or_mask

        # For each bit in n 0b11, map to float_bits [5, 0] = 0b10001 and set/clear
        for i in range(len(float_bits)):
          bit = float_bits[i]
          setbit = n>>i & 1
          clearbit = ~n>>i & 1
          memid2 |= setbit << bit
          memid2 &= ~(clearbit << bit)
        # print('store', memid2, bin(memid2), '=', v)
        mem[memid2] = v

  # print(mem)
  return sum(mem.values())

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
  float_mask = 0

  for i, ch in enumerate(mask[::-1]):
    if ch == '0':
      and_mask &= ~(1 << i)
    if ch == '1':
      or_mask |= 1 << i
    if ch == 'X':
      float_mask |= 1 << i
  
  # print(f'{and_mask:036b}')
  # print(f'{or_mask:036b}')
  return (and_mask, or_mask, float_mask)

def test_parse_mask():
  assert parse_mask( "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X") == (
                    0b111111111111111111111111111111111101,
                    0b000000000000000000000000000001000000,
                    0b111111111111111111111111111110111101
  )
  assert "Hello"[:1:-1] == "oll"
# To initialize your ferry's docking program, you need the sum of all values left in memory after the initialization program completes. (The entire 36-bit address space begins initialized to the value 0 at every address.) In the above example, only two values in memory are not zero - 101 (at address 7) and 64 (at address 8) - producing a sum of 165.
def test_part1(example1):
  assert part1(example1) == 165

# The entire 36-bit address space still begins initialized to the value 0 at every address, and you still need the sum of all values left in memory at the end of the program. In this example, the sum is 208.
def test_part2(example2):
  assert part2(example2) == 208

@pytest.fixture
def example1():
  return """mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0"""

@pytest.fixture
def example2():
  return """mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1"""
