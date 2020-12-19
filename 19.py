# Day 19: Monster Messages
import pytest

# How many messages completely match rule 0?
def part1(data):
  rules, messages = parse(data)

  matches = 0
  for message in messages:
    found = match(rules, message)
    if found == len(message):
      matches += 1

  return matches

def parse(data):
  [rules, messages] = data.split('\n\n')

  lam4 = lambda item: item.strip('"') if '"' in item else int(item)
  lam3 = lambda x: list(map(lam4, x.split(' ')))
  lam2 = lambda x: list(map(lam3, x.split(' | ')))
  lam1 = lambda x,y: (int(x), lam2(y))
  rules = dict(map(lambda x: lam1(*x.split(': ')), rules.split('\n')))
  messages = messages.split('\n')
  return rules, messages

def match(rules, message, rule_id = 0, pos = 0):
  # print('match', '>' * pos, message[pos:], rule_id, rules[rule_id])
  for either in rules[rule_id]:
    ok = True
    p1 = pos

    for every in either:
      if isinstance(every, int): 
        p2 = match(rules, message, every, p1)
        if p2 > p1:
          p1 = p2
        else:
          ok = False
          break
      elif isinstance(every, str):
        if message[p1] == every:
          p1 += 1
        else:
          ok = False
          break
      else:
        raise Exception('unknown type', rule_id, p1, every, either)
    
    # print('match', '<' * pos, message[pos:p1], rule_id, every, ok)

    if ok: return p1

  return pos
  
def test_match(rules1):
  rules, messages = parse(rules1)
  # Therefore, rule 0 matches aab or aba.
  assert match(rules, 'aab') == 3
  assert match(rules, 'aba') == 3
  assert match(rules, 'baa') == 0
  assert match(rules, 'abab') == 3

# In the above example, ababbb and abbbab match, but bababa, aaabbb, and aaaabbb do not, producing the answer 2.
def test_part1(example1):
  assert part1(example1) == 2

@pytest.fixture
def rules1():
  return """0: 1 2
1: "a"
2: 1 3 | 3 1
3: "b"

"""

@pytest.fixture
def rules2():
  return """0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

"""

@pytest.fixture
def example1():
  return """0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb"""
