'''
This is a template script for running TDNN simulations using the RunSim.py method
sys.path.extend(['/Users/se394/TDNN/py']) <-- add this to console to import

* This script was written to generate multiple parameters over a small number of iterations
'''
from joblib import Parallel, delayed
import multiprocessing, RunSim, initSim

__author__ = 'Shady'

# Initialize Simulation Parameters & Options
initSim = initSim.initSim()
# Set Parameters
initSim.params["ProjectPath"] = '/Users/shad/TDNN/py'
# # # DataSet Parameters
initSim.params['Category'] = 'consonants'
initSim.params['Shape'] = [65, 1]  # the shape will be nfft/2 + 1 for spectral data
initSim.params['SignaltoNoise'] = 1
# # # Simulation Parameters
initSim.params['NumIterations'] = 1  # number of times to loop over dataset
initSim.params['MaxDelay'] = 300  # make this the length of your pattern in ms
initSim.params['ThresholdRate'] = 0.95
initSim.params['InitialThresholdValue'] = 0.1
initSim.params['UpdateRate'] = 0.1
initSim.params['NumIterations'] = 1
initSim.params['NumDistributions'] = 10

# Set iterables
presentations = [10, 50, 100, 500, 1000]
trainingsets = ['t', 'g', 'k']
testingsets=['t', 'g', 'k']
numdistributions = [10]
snrs = [1]

# Run simulations in parallel
num_cores = multiprocessing.cpu_count()
print("numCores = " + str(num_cores))


# # # Define method for parallel iterable
def simTDNN(numpres):
    initSim.params['NumPresentations'] = numpres  # number of presentations within dataset
    for train in trainingsets:
        initSim.params['TrainingData'] = train
        for test in testingsets:
            initSim.params['TestingData'] = test
            for dist in numdistributions:
                initSim.params['NumDistributions'] = dist
                for snr in snrs:
                    initSim.params['SignaltoNoise'] = snr
                    # Run Simulation with Set Parameters
                    sim = RunSim.RunSim(initSim.params, initSim.options)
                    sim.go(initSim.params, initSim.options)


# # # Run
Parallel(n_jobs=num_cores)(delayed(simTDNN)(pres) for pres in presentations)
