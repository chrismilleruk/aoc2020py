# Day 4: Passport Processing 

# The expected fields are as follows:
expected_fields = {
  'byr': 'Birth Year',
  'iyr': 'Issue Year',
  'eyr': 'Expiration Year',
  'hgt': 'Height',
  'hcl': 'Hair Color',
  'ecl': 'Eye Color',
  'pid': 'Passport ID',
  'cid': 'Country ID' # optional
}
required_fields = list(expected_fields.keys())[:-1]

# Count the number of valid passports - those that have all required fields. Treat cid as optional. In your batch file, how many passports are valid?
def part1(data):
  import re
  passports = data.split('\n\n')
  valid = 0
  for passport in passports:
    fields = required_fields.copy()
    for match in re.finditer(r'(\w\w\w):', passport):
      field = match.groups()[0]
      if fields.count(field) > 0: fields.remove(field)
    if len(fields) == 0:
      valid +=1
  return valid

#   You can continue to ignore the cid field, but each other field has strict rules about what values are valid for automatic validation:

# byr (Birth Year) - four digits; at least 1920 and at most 2002.
# iyr (Issue Year) - four digits; at least 2010 and at most 2020.
# eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
# hgt (Height) - a number followed by either cm or in:
# If cm, the number must be at least 150 and at most 193.
# If in, the number must be at least 59 and at most 76.
# hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
# ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
# pid (Passport ID) - a nine-digit number, including leading zeroes.
# cid (Country ID) - ignored, missing or not.
