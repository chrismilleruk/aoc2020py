
# Find two numbers that sum to 2020, return the product.
def part1(data):
    steps = 0
    # Data is automatically read from 01.txt
    numbers = sorted(map(int, data.split()))
    i = 0
    j = len(numbers) -1
    while (i < j):
      a = numbers[i]
      b = numbers[j]
      c = a + b
      # print(i, j, a, b, c)
      if c == 2020: break
      if c > 2020: j -= 1
      if c < 2020: i += 1
      steps += 1
    return f"{a * b} in {steps} steps"

# Find three numbers that sum to 2020, return the product.
def part2(data):
  steps = 0
  numbers = sorted(map(int, data.split()))
  for i in range(0, len(numbers) - 3):
    j = i + 1
    k = len(numbers) -1
    while (j < k):
      a = numbers[i]
      b = numbers[j]
      c = numbers[k]
      d = a + b + c
      # print(i, j, k, a, b, c, d)
      if d == 2020: return f"{a * b * c} in {steps} steps"
      if d > 2020: k -= 1
      if d < 2020: j += 1
      steps += 1
    
  
