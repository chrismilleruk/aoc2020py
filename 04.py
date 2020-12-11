# Day 4: Passport Processing 

import re

# Count the number of valid passports - those that have all required fields. Treat cid as optional. In your batch file, how many passports are valid?
def part1(data):
  [required_fields, _] = define_fields()
  passports = data.split('\n\n')

  valid = 0
  for passport in passports:
    missing = required_fields.copy()
    for match in re.finditer(r'(\w\w\w):', passport):
      field = match.groups()[0]
      if missing.count(field) > 0: missing.remove(field)
    if len(missing) == 0:
      valid +=1
  return valid

# Count the number of valid passports - those that have all required fields and valid values. Continue to treat cid as optional. In your batch file, how many passports are valid?
def part2(data):
#   part2_test(part2_fn)
#   print('part2 self-check tests PASS')
#   return part2_fn(data)
#   # guess 1: 132 (high) - BUG: using match() instead of fullmatch()

# def part2_fn(data):
  [required_fields, validation_fns] = define_fields()
  passports = data.split('\n\n')
  valid = 0

  for passport in passports:
    valid_fields = set()
    for match in re.finditer(r'(\w\w\w):(\S+)', passport):
      [field, value] = match.groups()
      fn = validation_fns[field]
      # print('test', field, value, fn(value))
      if not fn(value): 
        # print(f'field {field} is invalid with value {value}', passport)
        break
      valid_fields.add(field)
    diff = valid_fields.symmetric_difference(required_fields)
    # print(passport, '\n', valid_fields, '\n', required_fields, '\n', diff, '\n\n')
    if diff == {'cid'} or len(diff) == 0:
      valid +=1

  return valid


def define_fields():
  #   You can continue to ignore the cid field, but each other field has strict rules about what values are valid for automatic validation:

  def validate_height(x):
    # hgt (Height) - a number followed by either cm or in:
    match = re.fullmatch(r'(\d+)cm$|(\d+)in', x)
    if match == None: return False

    [height_cm, height_in] = match.groups()
    # If cm, the number must be at least 150 and at most 193.
    if height_cm and int(height_cm) >= 150 and int(height_cm) <= 193: return True
    # If in, the number must be at least 59 and at most 76.
    if height_in and int(height_in) >= 59 and int(height_in) <= 76: return True
    return False

  # The expected fields are as follows:
  validation_fns = {
    # byr (Birth Year) - four digits; at least 1920 and at most 2002.
    'byr': lambda x: int(x) >= 1920 and int(x) <= 2002,
    # iyr (Issue Year) - four digits; at least 2010 and at most 2020.
    'iyr': lambda x: int(x) >= 2010 and int(x) <= 2020,
    # eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
    'eyr': lambda x: int(x) >= 2020 and int(x) <= 2030,
    # hgt (Height) - a number followed by either cm or in:  
    # If cm, the number must be at least 150 and at most 193.
    # If in, the number must be at least 59 and at most 76.
    'hgt': validate_height,
    # hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
    'hcl': lambda x: re.fullmatch(r'#[0-9a-f]{6}', x) != None,
    # ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
    'ecl': lambda x: re.fullmatch(r'amb|blu|brn|gry|grn|hzl|oth', x) != None,
    # pid (Passport ID) - a nine-digit number, including leading zeroes.
    'pid': lambda x: re.fullmatch(r'[0-9]{9}', x) != None,
    # cid (Country ID) - ignored, missing or not.
    'cid': lambda x: True
  }

  required_fields = list(validation_fns.keys())[:-1]

  return [required_fields, validation_fns]


def test_part2():
  # Here are some invalid passports:
  invalid_passports = """eyr:1972 cid:100
  hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

  iyr:2019
  hcl:#602927 eyr:1967 hgt:170cm
  ecl:grn pid:012533040 byr:1946

  hcl:dab227 iyr:2012
  ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

  hgt:59cm ecl:zzz
  eyr:2038 hcl:74454a iyr:2023
  pid:3556412378 byr:2007

  eyr:2029 ecl:bluz cid:129 byr:1989
  iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm"""

  assert part2(invalid_passports) is 0, f'some invalid passports were treated as valid.'
  
  # Here are some valid passports:
  valid_passports = """pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
  hcl:#623a2f

  eyr:2029 ecl:blu cid:129 byr:1989
  iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

  hcl:#888785
  hgt:164cm byr:2001 iyr:2015 cid:88
  pid:545766238 ecl:hzl
  eyr:2022

  iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719"""

  assert part2(valid_passports) is len(valid_passports.split('\n\n')), f'some valid passports were treated as invalid.'
  