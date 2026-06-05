'''
Initialize Parameters & Options for TDNN Simulation
'''
__author__ = 'Shady'


class initSim:
    def __init__(self):
        '''
        Constructor for initSim Class
        :return:
        '''
        # ---------------------------------------------------------------------------------------------------------
        #                                           DEFAULT SIMULATION OPTIONS
        # The simulation options encompass all possible datasets and types of simulations that can be run in TDNN.
        # Use the options field to set up batch simulations.
        self.options = dict()
        self.options['Category'] = ['simple-images', 'consonants', 'vowels', 'syllables']
        self.options['DataSets'] = ['x', 'chevron-l', 'chevron-r', 'simple_1', 'simple']
        self.options['SNRs'] = ['NaN', -12, -10, -6, -2, -1, 0, 1, 2, 6, 10]
        self.options['DelayFunctions'] = ['Masquillier', 'Single-Beta-Distribution', 'Beta-Mixture']
        self.options['ThresholdFunctions'] = ['Fixed', 'Continuous Increase', 'Continuous Adaptive Maximum',
                                              'Contributing Maximum',
                                              'Contributing Increasing', 'Contributing Adaptive Maximum',
                                              'Contributing Adaptive Increase', 'TEST']
        # ---------------------------------------------------------------------------------------------------------
        #                                         DEFAULT SIMULATION PARAMETERS
        self.params = dict()
        self.params['ProjectPath'] = '/Users/se394/TDNN/py'
        self.params['Shape'] = [20, 1]
        self.params['Inhibition'] = True
        self.params['NumPresentations'] = 1
        self.params['NumIterations'] = 5
        self.params['Speed'] = 1
        self.params['DelayFunction'] = 3
        self.params['MaxDelay'] = 15
        self.params['NumDistributions'] = 3
        self.params['ThresholdFunction'] = 3
        self.params['InitialThresholdValue'] = 0.1
        self.params['ThresholdRate'] = 0.95
        self.params['UpdateRule'] = 5
        self.params['UpdateRate'] = 0.1
        self.params['PrintPotential'] = True
        self.params['Category'] = self.options['Category'][0]
        self.params['TrainingData'] = self.options['DataSets'][1]
        self.params['TestingData'] = self.options['DataSets'][1]
        self.params['SignaltoNoise'] = self.options['SNRs'][3]

        @property
        def project_path():
            return self.params['ProjectPath']

        @project_path.setter
        def project_path(path):
            self.params['ProjectPath'] = path

        @property
        def shape():
            return self.params['Shape']

        @shape.setter
        def shape(shape):
            self.params['Shape'] = shape
