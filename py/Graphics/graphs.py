import math

import numpy
import matplotlib.pyplot as plt

infile = open('/Users/shadyeldamaty/Dropbox/Projects/TDNN/py/weights.txt')
data = []
for line in infile.readlines():
    temp = []
    for item in line.split():
        item = item.replace(' ', '').replace(',', '')
        temp.append(item)
    data.append(temp)
data = data[2:]

#add mesq

def beta(alpha, beta, x):
    _beta_func = math.exp(math.lgamma(alpha + beta) - (math.lgamma(alpha) + math.lgamma(beta)))
    if x == 0 or x == 1:
        return 0
    else:
        return (((1 - x) ** (beta - 1)) * x ** (alpha - 1)) * _beta_func


x = []
for item in data:
    temp = []
    for i in range(1024):
        temp.append(beta(float(item[2]), float(item[3]), i / 1024))
    x.append(temp)
x = numpy.array(x)


#outfile.write(x)

fig = plt.figure()
ax = plt.contourf(x)
plt.show()
