# Day 8: Handheld Halting
import pytest

def part1(data):
  program = parse(data)
  state = execute(program)
  print(state)
  return state['acc']

def part2(data):
  return None

def parse(source):
  program = map(parse_inst, source.split('\n'))
  return list(program)

def parse_inst(line):
  return [line[0:3], int(line[3:])]

def execute(program):
  ptr = 0
  acc = 0
  msg = ""

  try:
    while True:
      if ptr >= len(program):
        raise Exception(f"pointer out of bounds. ptr={ptr}, len={len(program)}")
      instr = program[ptr]
      if len(instr) == 2:
        instr.append(1)
      else:
        instr[2] += 1
      if instr[2] > 1: break
      
      if instr[0] == 'jmp':
        ptr += instr[1]
      elif instr[0] == 'acc':
        acc += instr[1]
        ptr += 1
      elif instr[0] == 'nop':
        ptr += 1
      else:
        raise Exception(f'unknown command "{instr}" at pos {ptr}')
  except Exception as e:
    msg = e

  return {
    "ptr": ptr,
    "acc": acc,
    "mem": program,
    "msg": msg
  }

def test_execute():
  state = execute([['acc', 1], ['acc', 1], ['acc', 1]])
  assert state["acc"] == 3, state

  state = execute([['jmp', 3], ['acc', 1], ['acc', 1], ['acc', 1]])
  assert state["acc"] == 1, state

  state = execute([['acc', 1], ['acc', 1], ['acc', 1], ['jmp', -2]])
  assert state["acc"] == 3, state

def test_parse(example1):
  program = parse(example1)
  assert program[0] == ['nop', 0]
  assert program[1] == ['acc', 1]
  assert program[2] == ['jmp', 4]
  assert program[5] == ['acc', -99]

def test_part1():
  assert True is True

@pytest.fixture
def example1():
  return """nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6"""