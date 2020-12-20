# Day 19: Monster Messages
import pytest
import numpy as np

# How many messages completely match rule 0?
def part1(data):
  rules, messages = parse(data)
  matches = find_matches(rules, messages)
  return sum(matches)


# After updating rules 8 and 11, how many messages completely match rule 0?
def part2(data):
  rules, messages = parse(data)
  rules = update_rules_8_and_11(rules)
  matches = find_matches(rules, messages)
  return sum(matches)


def find_matches(rules, messages):
  matches = list(map(lambda message: match(rules, message) == len(message), messages))
  return matches

def gen_matches(rules, rule_id = 0, matches = []):
  print(rule_id, matches, rules[rule_id])
  
  for either in rules[rule_id]:
    matches.append([])
    for every in either:
      if isinstance(every, int): 
        matches[-1].append(gen_matches(rules, every))
      elif isinstance(every, str):
        matches[-1].append(every)
  return matches
    # rules_seen.add()

def parse(data):
  [rules, messages] = data.split('\n\n')

  lam4 = lambda item: item.strip('"') if '"' in item else int(item)
  lam3 = lambda x: list(map(lam4, x.split(' ')))
  lam2 = lambda x: list(map(lam3, x.split(' | ')))
  lam1 = lambda x,y: (int(x), lam2(y))
  rules = dict(map(lambda x: lam1(*x.split(': ')), rules.split('\n')))
  messages = messages.split('\n')
  return rules, messages

def match(rules, message, rule_id = 0, pos = 0, stack = []):
  stack += [rule_id]
  print('match', message[:pos], message[pos:], stack, rules[rule_id])
  for either in rules[rule_id]:
    ok = True
    p1 = pos

    for every in either:
      if isinstance(every, int): 
        p2 = match(rules, message, every, p1, stack)
        if p2 > p1:
          p1 = p2
        else:
          ok = False
          break
      elif isinstance(every, str):
        if p1 < len(message) and message[p1] == every:
          p1 += 1
        else:
          ok = False
          break
      else:
        raise Exception('unknown type', rule_id, p1, every, either)
    
    if ok:
      print('match', message[:pos], message[pos:p1], message[p1:], stack, every, '=', ok)

    if ok: return p1

  return pos
  

def update_rules_8_and_11(rules):
  # 8: 42 | 42 8
  rules[8] = [[42], [42, 8]]
  # 11: 42 31 | 42 11 31
  rules[11] = [[42, 31], [42, 11, 31]]
  return rules


def test_match(rules1):
  rules, messages = parse(rules1)
  # Therefore, rule 0 matches aab or aba.
  assert match(rules, 'aab') == 3
  assert match(rules, 'aba') == 3
  assert match(rules, 'baa') == 0
  assert match(rules, 'abab') == 3

# def test_gen_matches(rules1):
#   rules, messages = parse(rules1)
#   matches = gen_matches(rules)
#   print(matches)
#   assert False

# In the above example, ababbb and abbbab match, but bababa, aaabbb, and aaaabbb do not, producing the answer 2.
def test_part1(example1):
  assert part1(example1) == 2

def test_example2(example2):
  assert part1(example2) == 3
  # assert part2(example2) == 12

def test_match2(example2):
  rules, messages = parse(example2)

  # Without updating rules 8 and 11, these rules only match three messages:  
  # bbabbbbaabaabba, ababaaaaaabaaab, and ababaaaaabbbaba.
  matches = find_matches(rules, messages)
  matches = np.array(messages)[matches]
  print(matches)
  np.testing.assert_equal(matches, [
    'bbabbbbaabaabba', 
    'ababaaaaaabaaab', 
    'ababaaaaabbbaba'])

  # However, after updating rules 8 and 11, a total of 12 messages match:
  rules = update_rules_8_and_11(rules)

  print('-' * 30)
  assert match(rules, 'babba', 42)
  assert match(rules, 'babbbbaa') > 0 
  assert match(rules, 'babbbbaabbbbbabbbbbbaabaaa') > 0 
  assert match(rules, 'babbbbaabbbbbabbbbbbaabaaabaaa') == 30
  assert False

  matches = find_matches(rules, messages)
  matches = np.array(messages)[matches]
  np.testing.assert_equal(matches, [
    'bbabbbbaabaabba', 
    'babbbbaabbbbbabbbbbbaabaaabaaa', 
    'aaabbbbbbaaaabaababaabababbabaaabbababababaaa', 
    'bbbbbbbaaaabbbbaaabbabaaa', 
    'bbbababbbbaaaaaaaabbababaaababaabab', 
    'ababaaaaaabaaab', 
    'ababaaaaabbbaba', 
    'baabbaaaabbaaaababbaababb', 
    'abbbbabbbbaaaababbbbbbaaaababb', 
    'aaaaabbaabaaaaababaa', 
    'aaaabbaabbaaaaaaabbbabbbaaabbaabaaa', 
    'aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba'])
  # bbabbbbaabaabba
  # babbbbaabbbbbabbbbbbaabaaabaaa
  # aaabbbbbbaaaabaababaabababbabaaabbababababaaa
  # bbbbbbbaaaabbbbaaabbabaaa
  # bbbababbbbaaaaaaaabbababaaababaabab
  # ababaaaaaabaaab
  # ababaaaaabbbaba
  # baabbaaaabbaaaababbaababb
  # abbbbabbbbaaaababbbbbbaaaababb
  # aaaaabbaabaaaaababaa
  # aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
  # aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba

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

@pytest.fixture
def example2():
  return """42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba"""