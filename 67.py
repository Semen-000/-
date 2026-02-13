import random

a = [random.randint(0, 10) for i in range(10)]
b = [random.randint(0, 10) for i in range(10)]

print(a)
print(b)

c = []
for i in b:
    if i not in a and i not in c:
        c.append(i)

for i in a:
    if i not in b and i not in c:
        c.append(i)
print(c)