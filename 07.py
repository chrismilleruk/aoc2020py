# Day 7: Handy Haversacks
import pytest 
import re

# How many bag colors can eventually contain at least one shiny gold bag? (The list of rules is quite long; make sure you get all of it.)
def part1(data):
  target = "shiny gold"
  rules = parse_rules(data)
  
  reverse_rules = dict()
  for parent, items in rules.items():
    for child, count in items.items():
      if child not in reverse_rules: 
        reverse_rules[child] = {}
      reverse_rules[child][parent] = count

  stack = [target]
  i = 0
  while i < len(stack):
    key = stack[i]
    if key in reverse_rules:
      stack.extend(reverse_rules[key].keys())
    i += 1

  stack = set(stack)
  # print(len(stack), stack)
  return len(stack) -1


# How many individual bags are required inside your single shiny gold bag?
def part2(data):
  target = "shiny gold"
  rules = parse_rules(data)
  cost = find_cost(rules, target)
  return cost - 1

def find_cost(rules, key):
  node = rules[key]
  cost = 1
  for key, value in node.items():
    cost += value * find_cost(rules, key)
  return cost

def parse_rules(data):
  return dict(map(parse_rule, data.split('\n')))

def parse_rule(line):
  match = re.match(
      r'(?P<description>[\s\w]+) bags contain (?P<contents>[\s\w\d,]+).',
      line)
  if match is None:
    raise Exception(f'regex does not match: {line}')
  key = match.group('description')
  contents = match.group('contents')
  o = [key, {}]
  if (contents != 'no other bags'):
    for item in contents.split(', '):
      match = re.match(r'(?P<count>\d+) (?P<description>[\s\w]+) bags?',
                      item)
      if match is None:
          raise Exception(f'regex does not match contents: {contents} {line}')
      d = match.groupdict()
      o[1][d['description']] = int(d['count'])
  return o


def test_part1(example1_data):
  # In the above rules, given a shiny gold bag, the following options would be available to you:
  # A bright white bag, which can hold your shiny gold bag directly.
  # A muted yellow bag, which can hold your shiny gold bag directly, plus some other bags.
  # A dark orange bag, which can hold bright white and muted yellow bags, either of which could then hold your shiny gold bag.
  # A light red bag, which can hold bright white and muted yellow bags, either of which could then hold your shiny gold bag.
  # So, in this example, the number of bag colors that can eventually contain at least one shiny gold bag is 4.
  assert part1(example1_data) == 4

def test_part2(example2_data):
  # In this example, a single shiny gold bag must contain 126 other bags.
  assert part2(example2_data) == 126

def test_parse_rule():
  assert parse_rule(
      'light red bags contain 1 bright white bag, 2 muted yellow bags.') == [
          "light red", {
              "bright white": 1,
              "muted yellow": 2
          }
      ]
  assert parse_rule('bright white bags contain 1 shiny gold bag.') == [
      "bright white", {
          "shiny gold": 1
      }
  ]
  assert parse_rule(
      'muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.') == [
          "muted yellow", {
              "shiny gold": 2,
              "faded blue": 9
          }
      ]

def test_find_cost(example2_data):
  rules = parse_rules(example2_data)
  assert find_cost(rules, 'dark violet') == 1
  assert find_cost(rules, 'dark blue') == 3
  assert find_cost(rules, 'dark green') == 7
  assert find_cost(rules, 'dark yellow') == 15
  assert find_cost(rules, 'dark orange') == 31
  assert find_cost(rules, 'dark red') == 63
  assert find_cost(rules, 'shiny gold') == 127

@pytest.fixture
def example1_data():
  return """light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags."""

@pytest.fixture
def example2_data():
  return """shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags."""
