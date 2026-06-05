# Import Modules for Time Delay Learning
__author__ = 'Shady'
from Networks import FeedForward
from py import options
from Updates import Variables  # use this to index variable functions
import time
import getpass
import os
# ---------------------------------------------------------------------------------------------------------
#                                           SIMULATION OPTIONS

maxdelay = 15
numdist = 3
delayfunction = 3

options=options.Options()
options['shape_vector'] = [20, 1]                                               #****************
options['max_delay'] = maxdelay                                                 #****************
options['delay_function'] = delayfunction
options['threshold_function'] = 3
options['threshold_start'] = 0.1
options['threshold_rate'] = 0.9
options['variable_function'] = 5
options['variable_rate'] = .1
options['number_of_distributions'] = numdist

dfs = ['Masquillier', 'Single-Beta-Distribution', 'Beta-Mixture']
thfs = ['Fixed', 'Continuous Increase', 'Continuous Adaptive Maximum', 'Contributing Maximum',
        'Contributing Increasing', 'Contributing Adaptive Maximum', 'Contributing Adaptive Increase', 'TEST']
# ---------------------------------------------------------------------------------------------------------
#                                               ENV VARS
path2proj = '/opt/TDNN/py'

#                                             DATASET VARS
category='simple-images'
datasets = ['x', 'chevron-l', 'chevron-r', 'simple_1', 'simple']
SNR = ['NaN', -10]
NUMPRES = 1
SNR = SNR[0]
# ---------------------------------------------------------------------------------------------------------
#                                        METADATA & OUTPUT PATHS

num_iterations = 5                                                            #***************
np=NUMPRES*num_iterations
runthisdataset = datasets[1]
#testthisdataset=''
testthisdataset = datasets[2]

# -------------------
# Define Datapaths
#path2data = '%s/Datasets/%s/%s_SNR%s_%dpres.txt' % (path2proj, category, runthisdataset, SNR, NUMPRES)
path2tdata='simple_R_noise.txt'
#path2tdata = '%s/Datasets/%s/%s_SNR%s_%dpres.txt' % (path2proj, category, testthisdataset, SNR, NUMPRES)
path2data='simple_L_noise.txt'
# -------------------
# Define Outputs
dst = '%s/simulations/%s-2/%s_SNR%s_%dpres' % (path2proj, category, runthisdataset, SNR, NUMPRES*num_iterations)
# Define training, test and parameter file paths/names
if testthisdataset:
    trainingprefix = '%s/TRAINTEST-%s-%ddelay-%ddists' % (dst, dfs[delayfunction-1], maxdelay, numdist)
else:
    trainingprefix = '%s/training-%s-%ddelay-%ddists' % (dst, dfs[delayfunction-1], maxdelay, numdist)
testprefix = '%s/teston-%s-%s-%ddelay-%ddists' % (dst, testthisdataset, dfs[delayfunction-1], maxdelay, numdist)
path2params = '%s/parameters-%s-%ddelay-%sdist.txt' % (dst, dfs[delayfunction-1], maxdelay, numdist)

# Create new results, overwrite old
if not os.path.exists(dst):
    print(dst)
    os.makedirs(dst)

now = time.strftime("%c")

print('\nRunning              ::  %s ' % runthisdataset)
print('Time Started         :: %s' % now)
print('Delay Function       ::  %s ' % dfs[delayfunction-1])
print('Total Presentations  ::  %s ' % np)
print('Max Delay            ::  %d ' % maxdelay)
print('# Distributions      ::  %d ' % numdist)
print('Test Data            ::  %s ' % testthisdataset)
print('SNR                  ::  %s' % SNR)
print('Training Output      ::  %s ' % trainingprefix)
print('Test Output          ::  %s ' % testprefix)
print('Parameter File       ::  %s \n\n' % path2params)

# ---------------------------------------------------------------------------------------------------------
#                                           TRAIN NOW!

net = FeedForward(options, trainingprefix)          # feed options object to network constructor

for i in range(num_iterations):
    print('iteration ' + str(i + 1))                # print iteration number
    net.run(path2data, trainingprefix)                              # run network

weightsfile = '%s_weights.txt' % trainingprefix

a = open(weightsfile, 'w')                        # write weights
a.write(net[(1, 0)].mixture_matrix)

# ---------------------------------------------------------------------------------------------------------
#                                           TEST NETWORK

if testthisdataset:
    print('\n testing')
    net = FeedForward(options, testprefix)          # feed options object to network constructor
    net.run(path2tdata, testprefix)                  # test network
    weightsfile = '%s_weights.txt' % testprefix
    a = open('weights-test.txt', 'w')                        # write weights
    a.write(net[(1, 0)].mixture_matrix)

# ---------------------------------------------------------------------------------------------------------
#                                     WRITE SIMULATION PARAMETERS

now = time.strftime("%c")

paramtxt = open(path2params, 'a')
paramtxt.write(
    "Simulation Parameters\n-------------------------------- \n ** run by %s -- %s\n\n" % (getpass.getuser(), now))
paramtxt.write("DataSet                    ::  %s " % runthisdataset)
paramtxt.write("Shape Vector               ::  %s\n" % options['shape_vector'])
paramtxt.write("Max Delay                  ::  %s\n" % options['max_delay'])
paramtxt.write("Delay Function             ::  %s\n" % dfs[options['delay_function']-1])
paramtxt.write("Threshold Function         ::  %s\n" % thfs[options['threshold_function']])
paramtxt.write("Threshold Start            ::  %s\n" % options['threshold_start'])
paramtxt.write("Threshold Rate             ::  %s\n" % options['threshold_rate'])
paramtxt.write("Variable Function          ::  %s\n" % Variables.updates(options['delay_function'],
                                                                         options['variable_function']))
paramtxt.write("Variable Rate              ::  %s\n" % options['variable_rate'])
paramtxt.write("Number of Distributions    ::  %s\n" % options['number_of_distributions'])
paramtxt.write("Number of Iterations       ::  %s\n" % np)
if not path2tdata:
    paramtxt.write("TESTED AGAINST             ::  %s\n" % path2tdata)
