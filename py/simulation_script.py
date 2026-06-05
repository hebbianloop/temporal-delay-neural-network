'''
This is a template script for running TDNN simulations using the RunSim.py method
sys.path.extend(['/Users/se394/TDNN/py']) <-- add this to console to import

* This script was written to generate multiple parameters over a small number of iterations
'''

from joblib import Parallel, delayed
import multiprocessing, RunSim, initSim

__author__ = 'Shady'

# Set iterables
trainingsets = ['chevron-l', 'chevron-r', 'x']
testingsets = ['chevron-r', 'chevron-l', 'x']
numdistributions = [1, 5, 10, 20, 30, 40]
snrs = ['NaN', -6]
iterations = [5,10]

# Initialize Simulation Parameters & Options
initSim = initSim.initSim()

# Set Parameters
initSim.params["ProjectPath"] = '/Users/shad/TDNN/py'
# # # DataSet Parameters
initSim.params['Category'] = 'simple-images'
initSim.params['Shape'] = [17, 1]  # the shape will be nfft/2 + 1 for spectral data
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
def simTDNN(training):
    initSim.params['TrainingData'] = training
    for test in testingsets:
        for dist in numdistributions:
            for snr in snrs:
                for iter in iterations:
                    initSim.params['NumIterations'] = iter  # number of times to loop over dataset
                    initSim.params['TestingData'] = test
                    initSim.params['NumDistributions'] = dist
                    initSim.params['SignaltoNoise'] = snr
                    # Run Simulation with Set Parameters
                    sim = RunSim.RunSim(initSim.params, initSim.options)
                    sim.go(initSim.params, initSim.options)

# # # Run
Parallel(n_jobs=num_cores)(delayed(simTDNN)(trainon) for trainon in trainingsets)
