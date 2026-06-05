import math

import numpy
import matplotlib.pyplot as plt

infile = open('../weights.txt')
data = []
for line in infile.readlines():
    temp = []
    for item in line.split():
        item = item.replace(' ', '').replace(',', '')
        temp.append(item)
    data.append(temp[2:])
data = data[2:]


def beta(alpha, beta, x):
    _beta_func = math.exp(math.lgamma(alpha + beta) - (math.lgamma(alpha) + math.lgamma(beta)))
    if x == 0 or x == 1:
        return 0
    else:
        return (((1 - x) ** (beta - 1)) * x ** (alpha - 1)) * _beta_func


x = []
for item in data:
    temp = []
    for i in range(100):
        value = 0
        for j in range(len(item)):
            if j % 2 == 0 and j < len(item):
                value += beta(float(item[j]), float(item[j + 1]), i / 100)
        value /= (len(item)/2)  ## SHADY EDIT -- if you are taking the average of betas then you should divide by the
                                # number of betas not by the number of parameters...
        temp.append(value)
    x.append(temp)
x = numpy.array(x)

fig = plt.figure()
ax = plt.contourf(x)
plt.show()
value = []
# a = 4
# for i in range(100):
#    value.append(beta(float(data[6][a]), float(data[6][a+1]), i/100))

# for x in value:
#   print(x)
total = 0
for line in data:
    total += sum([float(item) for item in line])
print(total)
