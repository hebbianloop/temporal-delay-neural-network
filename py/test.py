import options
from Networks import FeedForward

__author__ = 'James'
prefix = 'l_clean_mixture'

def test(infile, no_iterations):
    net = FeedForward(options.Options(), prefix)
    for i in range(no_iterations):
        print('iteration ' + str(i+1))
        net.run(infile)

    a = open(prefix + '_weights.txt', 'w')
    a.write(net[(1, 0)].mixture_matrix)


test('Datasets/a.txt', 2)
# cProfile.run("test('datasets/gSNR0', 1)")
# test = data.Data('datasets/gSNR0')
# print(test.speed)
# print(test.examples[1])
# print(len(test.examples))
# print(len(test.attributes))
# for i, example in enumerate(test.examples):
#  if len(example) == 1024:
#     print(i)
