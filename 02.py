# To try to debug the problem, they have created a list (your puzzle input) of passwords (according to the corrupted database) and the corporate policy when that password was set.

# For example, suppose you have the following list:

# 1-3 a: abcde
# 1-3 b: cdefg
# 2-9 c: ccccccccc
# Each line gives the password policy and then the password. The password policy indicates the lowest and highest number of times a given letter must appear for the password to be valid. For example, 1-3 a means that the password must contain a at least 1 time and at most 3 times.

# In the above example, 2 passwords are valid. The middle password, cdefg, is not; it contains no instances of b, but needs at least 1. The first and third passwords are valid: they contain one a or nine c, both within the limits of their respective policies.

# How many passwords are valid according to their policies?
def part1(data):
  valid = 0
  import re
  for entry in data.split('\n'):
    match = re.search('(?P<min>\d+)-(?P<max>\d+) (?P<letter>\w): (?P<password>.*)', entry)
    (min, max, letter, password) = match.groups()
    # print(min, max, letter, password)
    count = 0
    for ch in password:
      if ch == letter: count += 1
    if count >= int(min) and count <= int(max): valid += 1
  return valid

# Each policy actually describes two positions in the password, where 1 means the first character, 2 means the second character, and so on. (Be careful; Toboggan Corporate Policies have no concept of "index zero"!) Exactly one of these positions must contain the given letter. Other occurrences of the letter are irrelevant for the purposes of policy enforcement.

# Given the same example list from above:

# 1-3 a: abcde is valid: position 1 contains a and position 3 does not.
# 1-3 b: cdefg is invalid: neither position 1 nor position 3 contains b.
# 2-9 c: ccccccccc is invalid: both position 2 and position 9 contain c.

# How many passwords are valid according to the new interpretation of the policies?
def part2(data):
  valid = 0
  import re
  for entry in data.split('\n'):
    match = re.search('(?P<min>\d+)-(?P<max>\d+) (?P<letter>\w): (?P<password>.*)', entry)
    (min, max, ch, password) = match.groups()
    [i, j] = map(lambda x: password[int(x)-1], [min, max])
    if (i != j and ch in [i, j]): valid += 1
  return valid