# Day 16: Ticket Translation
import pytest
import numpy as np

# Consider the validity of the nearby tickets you scanned. What is your ticket scanning error rate?
def part1(data):
  validation_rules, ticket, nearby_tickets = parse(data)
  valid_ranges = np.concatenate(list(validation_rules.values()))
  def is_num_invalid(n):
    for r in valid_ranges:
      if n >= r[0] and n <= r[1]:
        return False
    return True
  
  invalid_nums = filter(is_num_invalid, np.concatenate(nearby_tickets))
  return sum(invalid_nums)

# Now that you've identified which tickets contain invalid values, discard those tickets entirely. Use the remaining valid tickets to determine which field is which.
# Once you work out which field is which, look for the six fields on your ticket that start with the word departure. What do you get if you multiply those six values together?
def part2(data, startsWith = 'departure'):
  rules, my_ticket, nearby_tickets = parse(data)
  valid_tickets = get_valid_tickets(nearby_tickets, rules)
  columns = identify_columns(rules, valid_tickets)
  completed_ticket = dict([(k,my_ticket[idx]) for k, idx in columns.items()])
  print(completed_ticket)
  return np.prod([v for k, v in completed_ticket.items() if k.startswith(startsWith)])

def identify_columns(rules, valid_tickets):
  columns_on_valid_tickets = np.stack(valid_tickets, axis=1)

  # Associate rules with columns on ticket data
  matching = [[] for _ in range(len(valid_tickets[0]))]
  for name, [[a,b], [c,d]] in rules.items():
    for idx, n in enumerate(columns_on_valid_tickets):
      # print(name, n, n >= a, n <= b, n >= c, n <= d, '-', 
      #   np.logical_and(n >= a, n <= b), np.logical_and(n >= c, n <= d), 
      #   np.logical_or(np.logical_and(n >= a, n <= b), np.logical_and(n >= c, n <= d)))
      if np.all(np.logical_or(np.logical_and(n >= a, n <= b), np.logical_and(n >= c, n <= d))):
        matching[idx] += [name]

  # Refine rules through a process of elimination.
  items = list(sorted(enumerate(matching), key=lambda x:len(x[1])))
  column_lookup = {}
  for idx, arr in items:
    if len(arr) > 1:
      print(items)
      raise Exception('ambiguous keys in rules')
    
    key = arr[0]
    for _, a in items:
      if a.count(key) > 0:
        a.remove(key)
    column_lookup[key] = idx
  return column_lookup


def get_valid_tickets(tickets, validation_rules):
  valid_ranges = np.concatenate(list(validation_rules.values()))

  return list(filter(lambda ticket: all(map(lambda x: in_ranges(x, valid_ranges), ticket)), tickets))

def in_ranges(n, ranges):
  for r in ranges:
    if n >= r[0] and n <= r[1]:
      return True
  return False
  
def parse(data):
  parts = data.split('\n\n')
  rules = dict(map(lambda r: r.split(': '), parts[0].split('\n')))
  for name, rule in rules.items():
    rules[name] = list(map(lambda r: list(map(int, r.split('-'))), rule.split(' or ')))
  ticket = parse_ticket(parts[1].split('your ticket:\n')[1])
  nearby_tickets = list(map(parse_ticket, parts[2].split('\n')[1:]))
  return rules, ticket, nearby_tickets

def parse_ticket(ticket):
  return list(map(int, ticket.split(',')))

# It doesn't matter which position corresponds to which field; you can identify invalid nearby tickets by considering only whether tickets contain values that are not valid for any field. In this example, the values on the first nearby ticket are all valid for at least one field. This is not true of the other three nearby tickets: the values 4, 55, and 12 are are not valid for any field. Adding together all of the invalid values produces your ticket scanning error rate: 4 + 55 + 12 = 71.
def test_part1(example1):
  assert part1(example1) == 71

def test_get_valid_tickets(example1):
  rules, ticket, nearby_tickets = parse(example1)
  assert get_valid_tickets(nearby_tickets, rules) == [[7,3,47]]

def test_part2(example2):
  rules, my_ticket, nearby_tickets = parse(example2)
  valid_tickets = get_valid_tickets(nearby_tickets, rules)
  columns = identify_columns(rules, valid_tickets)
  completed_ticket = dict([(k,my_ticket[idx]) for k, idx in columns.items()])
  assert completed_ticket == {'class': 12, 'row': 11, 'seat': 13}

  assert part2(example2, '') == 12 * 11 * 13

@pytest.fixture
def example1():
  return """class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12"""

@pytest.fixture
def example2():
  return """class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9"""
