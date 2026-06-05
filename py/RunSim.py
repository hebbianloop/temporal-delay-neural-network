'''
Class Object for Running a TDNN Simulation With Custom Parameters & Options
'''
# Import Modules for Time Delay Learning

__author__ = 'Shady'


class RunSim:
    def __init__(self, simparams, simoptions):
        '''
        The Constructor For run_simulation
        :param simparams:
        :param simoptions:
        :return:
        '''

        self.TrainingData = '%s/Datasets/%s/%s_SNR%s_%dpres.input' % (simparams['ProjectPath'], simparams['Category'],
                                                                      simparams['TrainingData'],
                                                                      simparams['SignaltoNoise'],
                                                                      simparams['NumPresentations'])
        self.TestingData = '%s/Datasets/%s/%s_SNR%s_%dpres.input' % (simparams['ProjectPath'], simparams['Category'],
                                                                     simparams['TestingData'],
                                                                     simparams['SignaltoNoise'],
                                                                     simparams['NumPresentations'])
        self.SimResultsDir = '%s/simulations/%s/%s_SNR%s_%dpres' % (simparams['ProjectPath'],
                                                                    simparams['Category'],
                                                                    simparams['TrainingData'],
                                                                    simparams['SignaltoNoise'],
                                                                    simparams['NumPresentations'] *
                                                                    simparams['NumIterations'])
        if simparams['TestingData']:
            self.TrainSimResults = '%s/TRAIN&TEST_%s-%ddelay-%ddist' % (self.SimResultsDir,
                                                                        simoptions['DelayFunctions'][
                                                                            simparams['DelayFunction'] - 1],
                                                                        simparams['MaxDelay'],
                                                                        simparams['NumDistributions']
                                                                        )
        else:
            self.TrainSimResults = '%s/TRAIN_%s-%ddelay-%ddist' % (self.SimResultsDir,
                                                                   simoptions['DelayFunctions'][
                                                                       simparams['DelayFunction'] - 1],
                                                                   simparams['MaxDelay'],
                                                                   simparams['NumDistributions']
                                                                   )

        self.TestSimResults = '%s/TEST_%s-%s-%ddelay-%ddist' % (self.SimResultsDir, simparams['TestingData'],
                                                                simoptions['DelayFunctions'][
                                                                    simparams['DelayFunction'] - 1],
                                                                simparams['MaxDelay'], simparams['NumDistributions'])
        self.ParamsFile = '%s/params_%s-%ddelay-%ddist.txt' % (self.SimResultsDir,
                                                               simoptions['DelayFunctions'][
                                                                   simparams['DelayFunction'] - 1],
                                                               simparams['MaxDelay'],
                                                               simparams['NumDistributions'])

    def go(self, simparams, simoptions):
        '''
        :param simparams:
        :param simoptions:
        :return:
        '''
        import os
        import time
        # Time started
        tstart = time.strftime("%c")
        # Create new results, overwrite old
        if not os.path.exists(self.SimResultsDir):
            print('Making Directory : ' + self.SimResultsDir)
            os.makedirs(self.SimResultsDir)
        # Print Simulation Parameters
        self.printSimParams(simparams, simoptions)
        # Train Neural Network With Parameters
        net = self.train(simparams)
        # Test Trained Network
        self.test(net)
        # Write Time Completed
        tcompl = time.strftime("%c")
        print('\n\nTime Completed    ::     %s\n\n' % tcompl)
        # Write Simulation Data & Parameters
        self.writeSimParams(simparams, simoptions, tstart, tcompl)

    def printSimParams(self, simparams, simoptions):
        '''
        Print Simulation Parameters to Console
        :param simparams:
        :param simoptions:
        :return:
        '''
        import time
        now = time.strftime("%c")
        print('\nRunning on           ::  %s ' % simparams['TrainingData'])
        print('Testing on           ::  %s ' % simparams['TestingData'])

        print('\n\nSimulation Parameters\n')
        print('Signal to Noise      ::  %s' % simparams['SignaltoNoise'])
        print('Total Presentations  ::  %s ' % (simparams['NumPresentations'] * simparams['NumIterations']))
        print('Delay Function       ::  %s ' % simoptions['DelayFunctions'][simparams['DelayFunction'] - 1])
        print('Max Delay            ::  %d ' % simparams['MaxDelay'])
        print('# Distributions      ::  %d ' % simparams['NumDistributions'])
        print('Threshold Function   ::  %s ' % simoptions['ThresholdFunctions'][simparams['ThresholdFunction'] - 1])
        print('Initial Threshold    ::  %f' % simparams['InitialThresholdValue'])
        print('Threshold Rate       ::  %f' % simparams['ThresholdRate'])

        print('\n\nOutput Files & Paths\n')
        print('Training Output      ::  %s ' % self.TrainSimResults)
        print('Test Output          ::  %s ' % self.TestSimResults)
        print('Parameter File       ::  %s' % self.ParamsFile)

        print('\n\nTime Started         ::  %s\n\n' % now)

    def setOptions(self, simparams):
        '''
        Set Network Level Options
        :param simparams:
        :return:
        '''
        import options
        options = options.Options()

        options['shape_vector'] = simparams['Shape']
        options['inhibitory'] = simparams['Inhibition']

        options['delay_function'] = simparams['DelayFunction']
        options['max_delay'] = simparams['MaxDelay']
        options['number_of_distributions'] = simparams['NumDistributions']

        options['threshold_function'] = simparams['ThresholdFunction']
        options['threshold_start'] = simparams['InitialThresholdValue']
        options['threshold_rate'] = simparams['ThresholdRate']

        options['variable_function'] = simparams['UpdateRule']
        options['variable_rate'] = simparams['UpdateRate']
        return (options)

    def train(self, simparams):
        '''
        Method for Network Training
        :param simparams:
        :param simoptions:
        :return:
        '''
        from Networks import FeedForward
        options = self.setOptions(simparams)
        net = FeedForward(options, self.TrainSimResults)

        for i in range(simparams['NumIterations']):
            print('iteration ' + str(i + 1))
            net.run(self.TrainingData, self.TrainSimResults)

        weightsfile = '%s_weights.txt' % self.TrainSimResults

        a = open(weightsfile, 'w')  # write weights
        a.write(net[(1, 0)].mixture_matrix)
        return net

    def test(self, net):
        '''
        Method for Network Testing
        :param options:
        :param simparams:
        :return:
        '''
        print('\n Running Test ..')
        from Networks import FeedForward

        net.run(self.TestingData, self.TestSimResults)
        weightsfile = '%s_weights.txt' % self.TestSimResults
        a = open(weightsfile, 'w')
        a.write(net[(1, 0)].mixture_matrix)
        return

    def writeSimParams(self, simparams, simoptions, tstart, tcomp):
        '''
        Method for Writing Simulation Parameters to Text File
        :param simparams:
        :param simoptions:
        :return:
        '''
        import getpass
        from Updates import Variables
        paramtxt = open(self.ParamsFile, 'a')
        paramtxt.write(
                "\n\nSimulation Parameters\n-------------------------------- \n ** run by %s -- %s\n\n" % (
                    getpass.getuser(), tstart))
        paramtxt.write("DataSet                    ::  %s " % self.TrainingData)
        paramtxt.write(
                "Number of Presentations     ::  %d\n" % simparams['NumIterations'] * simparams['NumPresentations'])
        paramtxt.write("Shape Vector               ::  %s\n" % simparams['Shape'])
        paramtxt.write("Inhibitory                 ::  %s\n" % simparams['Inhibition'])
        paramtxt.write(
                "Delay Function             ::  %s\n" % simoptions['DelayFunctions'][simparams['DelayFunction'] - 1])
        paramtxt.write("Max Delay                  ::  %s\n" % simparams['MaxDelay'])
        paramtxt.write("Number of Distributions    ::  %s\n" % simparams['NumDistributions'])
        paramtxt.write("Threshold Function         ::  %s\n" % simoptions['ThresholdFunctions'][
            simparams['ThresholdFunction'] - 1])
        paramtxt.write("Threshold Start            ::  %s\n" % simparams['InitialThresholdValue'])
        paramtxt.write("Threshold Rate             ::  %s\n" % simparams['ThresholdRate'])
        paramtxt.write("Variable Function          ::  %s\n" % Variables.updates(simparams['DelayFunction'],
                                                                                 simparams['UpdateRule']))
        paramtxt.write("Variable Rate              ::  %s\n" % simparams['UpdateRate'])
        paramtxt.write("TESTED AGAINST             ::  %s\n" % self.TestingData)
        paramtxt.write("\n~Time completed             ::  %s\n" % tcomp)
