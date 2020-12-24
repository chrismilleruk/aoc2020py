# Day 21: Allergen Assessment
import pytest

# Determine which ingredients cannot possibly contain any of the allergens in your list. How many times do any of those ingredients appear?
def part1(data):
  all_foods = parse(data)
  ingredients, allergens = get_lookups(all_foods)
  # Each allergen is found in exactly one ingredient. 
  # Each ingredient contains zero or one allergen. 
  # Allergens aren't always marked

  # Find safe ingredients
  safe, unsafe = safe_ingredients(allergens, ingredients.keys())

  # Counting the number of times any of these ingredients appear in any ingredients list produces 5: they all appear once each except sbzzf, which appears twice.
  count = sum(map(lambda f: len(safe.intersection(f.ingredients)), all_foods))
  return count

def part2(data):
  all_foods = parse(data)
  ingredients, allergens = get_lookups(all_foods)
  safe, unsafe = safe_ingredients(allergens, ingredients.keys())
  # Now that you've isolated the inert ingredients, you should have enough information to figure out which ingredient contains which allergen.

  # Filter allergens to potentially unsafe ingredients against each allergen
  known_ingredients = {}
  unsafe_set = set(unsafe)
  for a, f in allergens.items():
    potentially_unsafe_ingredients = [unsafe_set.intersection(food.ingredients) for food in f]
    allergens[a] = unsafe_set.intersection(*potentially_unsafe_ingredients)

    # If there is only one possible ingredient, add to known ingredients
    if len(allergens[a]) == 1:
      ingredient = next(iter(allergens[a]))
      known_ingredients[ingredient] = a

  changes = True
  while changes:
    changes = False
    # Remove known ingredients from potential ingredients against each allergen
    for key, values1 in allergens.items():
      if len(values1) > 1:
        values2 = values1.difference(known_ingredients.keys())
        if values1 != values2:
          changes = True
          allergens[key] = values2

          # If there is only one possible ingredient, add to known ingredients
          if len(values2) == 1:
            ingredient = next(iter(values2))
            known_ingredients[ingredient] = key

  print(known_ingredients)

  # Arrange the ingredients alphabetically by their allergen and separate them by commas to produce your canonical dangerous ingredient list. (There should not be any spaces in your canonical dangerous ingredient list.) 
  arranged_ingredients = map(lambda t: t[0], sorted(known_ingredients.items(), key = lambda t: t[1]))
  return ",".join(arranged_ingredients)

def parse(data):
  foods = list(map(lambda line: Food(line), data.split('\n')))
  return foods

def get_lookups(foods):
  ingredients, allergens = {}, {}
  for food in foods:
    for ingredient in food.ingredients:
      if ingredient not in ingredients:
        ingredients[ingredient] = []
      ingredients[ingredient].append(food)
    
    for allergen in food.allergens:
      if allergen not in allergens:
        allergens[allergen] = []
      allergens[allergen].append(food)
  return ingredients, allergens

def safe_ingredients(allergens, all_ingredients):
  unsafe_ingredients = []
  for allergen, foods in allergens.items():
    unsafe = set(all_ingredients).intersection(*map(lambda f: f.ingredients, foods))
    unsafe_ingredients += unsafe
  safe_ingredients = set(all_ingredients).difference(unsafe_ingredients)
  return safe_ingredients, set(unsafe_ingredients)


class Food():
  def __init__(self, line):
    (ingredients, allergens) = line.split(' (contains ')
    self.ingredients = ingredients.split(' ')
    self.allergens = allergens[:-1].split(', ')
  def __repr__(self):
    return f"Food({len(self.ingredients)}, {len(self.allergens)})"
  def __str__(self):
    return f"Food({len(self.ingredients)})"



def test_parse(example1):
  foods = parse(example1)
  assert isinstance(foods[0], Food)
  # assert foods[0] == Food('mxmxvkd kfcds sqjhc nhms (contains dairy, fish)')
  assert foods[0].ingredients == ['mxmxvkd', 'kfcds', 'sqjhc', 'nhms']
  assert foods[0].allergens == ['dairy', 'fish']

def test_safe_ingredients(example1):
  all_foods = parse(example1)
  ingredients, allergens = get_lookups(all_foods)
  safe, unsafe = safe_ingredients(allergens, ingredients.keys())
  # In the example, none of the ingredients kfcds, nhms, sbzzf, or trh can contain an allergen.
  assert safe == {'kfcds', 'nhms', 'sbzzf', 'trh'}

def test_part1(example1):
  # Counting the number of times any of these ingredients appear in any ingredients list produces 5: they all appear once each except sbzzf, which appears twice.
  assert part1(example1) == 5

def test_part2(example1):
  # Arrange the ingredients alphabetically by their allergen and separate them by commas to produce your canonical dangerous ingredient list. (There should not be any spaces in your canonical dangerous ingredient list.) In the above example, this would be mxmxvkd,sqjhc,fvjkl.
  assert part2(example1) == 'mxmxvkd,sqjhc,fvjkl'

@pytest.fixture
def example1():
  return """mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)"""