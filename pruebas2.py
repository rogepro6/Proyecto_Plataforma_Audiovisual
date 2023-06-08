from collections import defaultdict
from itertools import chain

d1 = {"Python": [1, 2], "C": [3, 4, 5]}
d2 = {"Java": [4], "C": [3]}

dict3 = defaultdict(list)
for k, v in chain(d1.items(), d2.items()):
    dict3[k].append(v)

print(dict3)
totales = []
for k, items in dict3.items():
    total = 0
    if k == "C":
        for item in items:
            total += len(item)
        totales.append(total)

print(totales)
