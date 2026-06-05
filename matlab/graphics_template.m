%% TEMPLATE SCRIPT FOR PLOTTING TDNN GRAPHICS
%  TODO: make this a function and pass the parameters to a higher level script

% project datafileectory
path2proj='/Users/se394/TDNN/';

% path to results
path2results=fullfile(path2proj,'py/simulations')

% output files
files2parse={'weights.txt','potential_log.txt'};

% dataset parameters
category={'simple-images','simple-images-2'};
patterns={'chevron-l','chevron-r','x','simple','simple_1'};
S2NR=[nan -12 -10 -6 -2 -1 0 1 2 6 10 12];

pattern=patterns{1};
category=category{1};
S2NR=S2NR(1);

numpres=50;
% load original data
datafile=fullfile(path2proj,'matlab','data',category, sprintf('%s_SNR%d_%dpres.mat',pattern,S2NR,numpres)); 
load(datafile)

numpres=150;
% path to simulation results
datafile=fullfile(path2proj,'py','simulations',category,sprintf('%s_SNR%d_%dpres', ...
        pattern,S2NR,numpres)); 

% ------------------------------------------------------------------------
% PLOT WEIGHTS -- Beta Mix
% ------------------------------------------------------------------------
printformat='pdf';
trainortest='TRAIN&TEST';
delayfunction='Beta-Mixture';
delaywin=300;
numdistributions=40;
% define file to load
filename=fullfile(datafile,sprintf('%s_%s-%idelay-%idist_%s',trainortest,delayfunction, ...
    delaywin, numdistributions, files2parse{1}));

% import weights data
 data = import_weights(filename);

% calculate beta mixture across inputs
[betamix, ~] = calc_Betamix(data);

savepicshere=fullfile(datafile,sprintf('%s_%s-%idelay-%idist_weights',trainortest,delayfunction, ...
    delaywin, numdistributions));
delaywin=0.2;           % delay window in seconds
% beta graphics
graphics_Betamix(betamix,savepicshere,delaywin,SGdata{2},printformat);

% ------------------------------------------------------------------------
% PLOT POTENTIAL
% ------------------------------------------------------------------------
savepicshere=fullfile(datafile,sprintf('%s_%s-%idelay-%idist_potential',trainortest,delayfunction, ...
    delaywin, numdistributions));
printformat='pdf';
delaywin=300;
% define file to load
filename=fullfile(datafile,sprintf('%s_%s-%ddelay-%idist_%s',trainortest,delayfunction, ...
    delaywin, numdistributions, files2parse{2}));

% Number of presentations
numpres=50;

% Duration of Stimulus
stimduration=nnz(stimtimes)/numpres;

% import potential data
data = import_potential(filename,1, inf);

presinwin=10;
% % potential graphics
graphics_potential(data, ts,stimtimes,stimduration, savepicshere,printformat,presinwin);

% ------------------------------------------------------------------------
% PLOT WEIGHTS -- Mesq
% ------------------------------------------------------------------------
%savepicshere=fullfile(datafile,'weights');
%printformat='pdf';
% define file to load
%filename=fullfile(datafile,files2parse{3});

% import weights data
%data = import_weights(filename);

% calculate mesequilier weights across inputs
%[mweights,~] = calc_Mesqweights(data);
%delaywin=0.07;           % delay window in seconds

% mesq graphics
%graphics_Mesq(meights,savepicshere,delaywin,F,printformat);

