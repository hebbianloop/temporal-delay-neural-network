'''
This is a template script for running TDNN simulations using the RunSim.py method
sys.path.extend(['/Users/se394/TDNN/py']) <-- add this to console to import

* This script was written to generate multiple parameters over a small number of iterations
'''
from joblib import Parallel, delayed
import multiprocessing, RunSim, initSim

__author__ = 'Shady'
# Set iterables
trainingsets = ['shady']
testingsets = ['shady']
numdistributions = [40]
snrs = ['NaN']
iterations = [500]
# Initialize Simulation Parameters & Options
initSim = initSim.initSim()
# Set Parameters
initSim.params["ProjectPath"] = '/Users/shad/TDNN/py'
# # # DataSet Parameters
initSim.params['Category'] = 'fun-images'
initSim.params['Shape'] = [65, 1]  # the shape will be nfft/2 + 1 for spectral data
# initSim.params['Shape'] = [129,1]                      # the shape will be nfft/2 + 1 for spectral data
initSim.params['NumPresentations'] = 1  # number of presentations within dataset
# # # Simulation Parameters
initSim.params['MaxDelay'] = 300  # make this the length of your pattern in ms
initSim.params['ThresholdRate'] = 0.95
initSim.params['InitialThresholdValue'] = 0.1
initSim.params['UpdateRate'] = 0.1

# Run simulations in parallel
num_cores = multiprocessing.cpu_count()
print("numCores = " + str(num_cores))


# # # Define method for parallel iterable
def simTDNN(iterations):
    initSim.params['NumIterations'] = iterations                            # parallelize iterations
    for train in trainingsets:
        initSim.params['TrainingData'] = train                              # loop over training sets linearly
        for test in testingsets:
            initSim.params['TestingData'] = test                            # loop over testing sets linearly
            for dist in numdistributions:
                initSim.params['NumDistributions'] = dist                   # loop over distributions linearly
                for snr in snrs:
                    initSim.params['SignaltoNoise'] = snr                   # loop over SNRs linearly
                    # Run Simulation with Set Parameters
                    sim = RunSim.RunSim(initSim.params, initSim.options)    # finally run with set parameters
                    sim.go(initSim.params, initSim.options)


Parallel(n_jobs=num_cores)(delayed(simTDNN)(iter) for iter in iterations)