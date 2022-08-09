from collections import Counter

num = int(input())

x = Counter([int(input()) for i in range(num)])

y = list((sorted(x.values())))

highestFrq = []
secondFrq = []

secondHigh = 0

if len(y) > 1:
    secondHigh = y[-2]
    high = y[-1]
else:
    high = y[-1]

for i in x.items():
    if i[1] == high:
        highestFrq.append(i[0])

    if i[1] == secondHigh:
        secondFrq.append(i[0])

if (len(highestFrq))>1:
    print(abs(max(highestFrq) - min(highestFrq)))
else:
    a = abs(max(highestFrq) - min(secondFrq))
    b = abs(min(highestFrq) - max(secondFrq))
    print(max((a, b)))

