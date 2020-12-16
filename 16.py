# Day 16: Ticket Translation
import pytest
import re
from functools import reduce
import numpy as np

# Consider the validity of the nearby tickets you scanned. What is your ticket scanning error rate?
def part1(data):
  validation_rules, ticket, nearby_tickets = parse(data)
  valid_ranges = np.concatenate(list(validation_rules.values()))
  def is_invalid(n):
    for r in valid_ranges:
      if n >= r[0] and n <= r[1]:
        return False
    return True

  invalid_nums = filter(is_invalid, map(int, re.split(r'[\n,]', nearby_tickets)))
  return sum(invalid_nums)

def parse(data):
  parts = data.split('\n\n')
  rules = dict(map(lambda r: r.split(': '), parts[0].split('\n')))
  for name, rule in rules.items():
    rules[name] = list(map(lambda r: list(map(int, r.split('-'))), rule.split(' or ')))
  ticket = parts[1].split('your ticket:\n')[1]
  nearby_tickets = parts[2].split('nearby tickets:\n')[1]
  return rules, ticket, nearby_tickets


# It doesn't matter which position corresponds to which field; you can identify invalid nearby tickets by considering only whether tickets contain values that are not valid for any field. In this example, the values on the first nearby ticket are all valid for at least one field. This is not true of the other three nearby tickets: the values 4, 55, and 12 are are not valid for any field. Adding together all of the invalid values produces your ticket scanning error rate: 4 + 55 + 12 = 71.
def test_part1(example1):
  assert part1(example1) == 71

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
