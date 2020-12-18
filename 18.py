# Day 18: Operation Order
import pytest
import re

# Evaluate the expression on each line of the homework; what is the sum of the resulting values?
def part1(data):
  total = 0
  for line in data.split('\n'):
    tokens = tokenize(line)
    program = parse(tokens)
    val = calc(program)
    print(val, '=', line)
    total += val

  return total

# Now, addition and multiplication have different precedence levels, but they're not the ones you're familiar with. Instead, addition is evaluated before multiplication.
def part2(data):
  return None

def tokenize(line):
  match = re.findall(r'\d+|\+|\*|\(|\)', line)
  return match
  
def parse(tokens, state = {'level': 0, 'pos': 0}):
  operators = ['+', '*']
  stack = [[]]

  for token in tokens:
    if token == '(':
      stack.append([])
    elif token == ')':
      assert len(stack) > 1, stack
      stack[-2].append(tuple(stack[-1]))
      stack = stack[:-1]
    elif token in operators:
      stack[-1].append(token)
    else:
      stack[-1].append(int(token))

  assert len(stack) == 1, stack
  result = tuple(stack[0]) 
  # print(result)
  return result


def calc(arr):
  if isinstance(arr, int):
    return arr

  total = calc(arr[0])
  for op, val in zip(arr[1::2], arr[2::2]):
    val = calc(val)

    if op == '+':
      total += val
    elif op == '-':
      total -= val
    elif op == '*':
      total *= val
    elif op == '/':
      total /= val
  return total


def test_calc():
  assert calc([1, '+', 1]) == 2
  # 1 + 2 * 3 + 4 * 5 + 6 == 71
  assert calc([1, '+', 2, '*', 3, '+', 4, '*', 5, '+', 6])== 71
  # 1 + (2 * 3) + (4 * (5 + 6)) == 51
  assert calc((1, '+', (2, '*', 3), '+', (4, '*', (5, '+', 6)))) == 51
  # Here are a few more examples:
  # 2 * 3 + (4 * 5) becomes 26.
  assert calc((2, '*', 3, '+', (4, '*', 5))) == 26
  # 5 + (8 * 3 + 9 + 3 * 4 * 3) becomes 437.
  # assert calc("5 + (8 * 3 + 9 + 3 * 4 * 3)") == 437
  # # 5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4)) becomes 12240.
  # assert calc("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))") == 12240
  # # ((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2 becomes 13632.
  # assert calc("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2") == 13632

def ntest_part1():
  # For example, the steps to evaluate the expression 1 + 2 * 3 + 4 * 5 + 6 are as follows:

  # 1 + 2 * 3 + 4 * 5 + 6
  #   3   * 3 + 4 * 5 + 6
  #       9   + 4 * 5 + 6
  #          13   * 5 + 6
  #              65   + 6
  #                  71
  assert part1("1 + 2 * 3 + 4 * 5 + 6") == 71
  # Parentheses can override this order; for example, here is what happens if parentheses are added to form 1 + (2 * 3) + (4 * (5 + 6)):

  # 1 + (2 * 3) + (4 * (5 + 6))
  # 1 +    6    + (4 * (5 + 6))
  #      7      + (4 * (5 + 6))
  #      7      + (4 *   11   )
  #      7      +     44
  #             51
  assert part1("1 + (2 * 3) + (4 * (5 + 6))") == 51

  # Here are a few more examples:
  # 2 * 3 + (4 * 5) becomes 26.
  assert part1("2 * 3 + (4 * 5)") == 26
  # 5 + (8 * 3 + 9 + 3 * 4 * 3) becomes 437.
  assert part1("5 + (8 * 3 + 9 + 3 * 4 * 3)") == 437
  # 5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4)) becomes 12240.
  assert part1("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))") == 12240
  # ((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2 becomes 13632.
  assert part1("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2") == 13632

@pytest.fixture
def example1():
  return "1 + 2 * 3 + 4 * 5 + 6"
