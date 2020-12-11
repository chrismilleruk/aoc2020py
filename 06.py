# Day 6: Custom Customs

# For each group, count the number of questions to which anyone answered "yes". What is the sum of those counts?
def part1(data):
  groups = data.split('\n\n')
  valid = set(map(chr, range(ord('a'), ord('z')+1)))

  def get_count(group):
    s = set()
    for ch in group:
      if ch in valid: s.add(ch)
    return len(s)

  return sum(map(get_count, groups))

# You don't need to identify the questions to which anyone answered "yes"; you need to identify the questions to which everyone answered "yes"!
# For each group, count the number of questions to which everyone answered "yes". What is the sum of those counts?
def part2(data):
  groups = data.split('\n\n')
  valid = set(map(chr, range(ord('a'), ord('z')+1)))

  def get_count(group):
    s = valid.copy()
    for line in group.split('\n'):
      s.intersection_update(set(line)) 
    return len(s)

  return sum(map(get_count, groups))


def test_part1():
  s = set()
  s.add('a')
  s.add('a')
  assert s == {'a'}
