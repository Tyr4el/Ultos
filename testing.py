import itertools
import random

fruits = ['🍒', '🍇', '🍐', '🍎', '🍋', '🍈', '🍑', '🍊']
results = [fruit for fruit in random.choices(fruits, k=5)]
grouped_fruits = [len(list(g)) for k, g in itertools.groupby(results)]
print(results)
print(grouped_fruits)
print(max(grouped_fruits))