import RunSim, initSim
__author__ = 'Shady'

# Initialize Simulation Parameters & Options
initSim = initSim.initSim()
# Set Parameters
initSim.params["ProjectPath"] = '/Users/shad/TDNN/py'
# # # DataSet Parameters
initSim.params['Category'] = 'simple-images'
initSim.params['TrainingData'] = 'x'
initSim.params['TestingData'] = ''
initSim.params['Shape'] = [17, 1]  # the shape will be nfft/2 + 1 for spectral data
initSim.params['NumPresentations'] = 1  # number of presentations within dataset
# # # Simulation Parameters
initSim.params['MaxDelay'] = 300  # make this the length of your pattern in ms
initSim.params['ThresholdRate'] = 0.95
initSim.params['InitialThresholdValue'] = 0.1
initSim.params['UpdateRate'] = 0.01
initSim.params['NumIterations'] = 6   # number of times to loop over dataset
initSim.params['NumDistributions'] = 10
initSim.params['SignaltoNoise'] = 'NaN'
# Run Simulation with Set Parameters
sim = RunSim.RunSim(initSim.params, initSim.options)
sim.go(initSim.params, initSim.options)

