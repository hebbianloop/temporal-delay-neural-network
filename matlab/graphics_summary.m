function graphics_summary(projectpath,category,trainedpattern,testpattern,S2NR,numiter,numpres,delaywin,numdist)
% -------------------------------------------------------------------------------
% 								 Default Arguments
%
% set simulation parameters
fprintf('\n\n📝 Summary Graphics\n\n')
fprintf('\n------------------------------\n')
fprintf('\nTraining Pattern    ::  %s\n',trainedpattern)
fprintf('\nTesting Pattern     ::  %s\n',testpattern)
fprintf('\nSignal to Noise     ::  %d\n',S2NR)
fprintf('\nNum Presentations   ::  %d\n',numiter*numpres)
fprintf('\nDelay Window        ::  %d\n',delaywin)
fprintf('\nDistributions       ::  %d\n',numdist)
numsimpres=numiter*numpres;
fprefix='TRAIN&TEST';
delayfun='Beta-Mixture';
printformat='pdf';
% set results path
resultspath=fullfile(projectpath,'py/simulations',category,sprintf('%s_SNR%d_%dpres',trainedpattern,S2NR,numsimpres));
% get training data
trainingdata=fullfile(projectpath,'matlab','data',category,sprintf('%s_SNR%d_%dpres.mat',trainedpattern,S2NR,numpres));
load(trainingdata)
% -------------------------------------------------------------------------------
% 							 Plot Weights for Beta Mix
%
% import weights data
filename = fullfile(resultspath,sprintf('%s_%s-%idelay-%idist_weights.txt',fprefix,delayfun,delaywin,numdist));
fprintf('\n\nImporting Weights Data ...');
filename
data     = import_weights(filename);
% calculate beta mixture across inputs
[betamix, ~] = calc_Betamix(data);
% define path for saving data
fprintf('\tPlotting Weights Data ...');
savepicshere=fullfile(resultspath,sprintf('%s_%s-%idelay-%idist_weights',fprefix,delayfun,delaywin,numdist));
% generate graphics
graphics_Betamix(betamix,savepicshere,delaywin/1000,SGdata{2},printformat)
% -------------------------------------------------------------------------------
% 								Plot Potential Plot
%
% import potential data
filename = fullfile(resultspath,sprintf('%s_%s-%idelay-%idist_potential_log.txt',fprefix,delayfun,delaywin,numdist));
filename
fprintf('\tImporting Potential Data ...');
traindata = import_potential(filename,1,inf);
% determine duration of stimulus
stimduration = nnz(stimtimes)/numpres;
% define path for saving data
savepicshere=fullfile(resultspath,sprintf('%s_%s-%idelay-%idist_potential',fprefix,delayfun,delaywin,numdist));
% generate potential graphics
fprintf('\tPlotting Potential Data ...');
graphics_potential(traindata,ts,stimtimes,stimduration,savepicshere,printformat);
% redefine so don't overwrite...
ts1=ts;
stimtimes1=stimtimes;
stimduration1=stimduration;
% -------------------------------------------------------------------------------
% 								Plot Potential TESTING Plot
%
%fprefix=sprintf('TEST_%s',testpattern);
% get testing data (tested on same parameters)
%testingdata=fullfile(projectpath,'matlab','data',category,sprintf('%s_SNR%d_%dpres.mat',testpattern,S2NR,numpres));
%load(testingdata)
% import potential data
%filename = fullfile(resultspath,sprintf('%s-%s-%idelay-%idist_potential_log.txt',fprefix,delayfun,delaywin,numdist));
%fprintf('\tImporting Potential Data ...');
%testdata = import_potential(filename,1,inf);
% determine duration of stimulus
%stimduration = nnz(stimtimes)/numpres;
% define path for saving data
%savepicshere=fullfile(resultspath,sprintf('TESTPLOT_%s_%s-%idelay-%idist_potential',fprefix,delayfun,delaywin,numdist));
% generate potential graphics
%fprintf('\tPlotting Potential Data on Test ...\n\n');
%graphics_potential_trainvstest(traindata,testdata,ts1,ts,stimtimes1,stimtimes,stimduration1,stimduration,savepicshere,printformat);
