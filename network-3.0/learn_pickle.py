from multiprocessing.dummy import Pool as ThreadPool

pool = ThreadPool(4) # Sets the pool size to 4

number = 5
w = 0
for i in range(number):
    w += 2
print(w)

def test(dummy):
    return 2
p = pool.map(test,range(number))

