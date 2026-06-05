% output files
files2parse={'weights.txt','potential_log.txt','weights.txt','m-weights.txt'};

% dataset parameters
category={'simple-images','simple-images-2'};
patterns={'chevron-l','chevron-r','x','simple','simple_1'};
S2NR=nan;

pattern=patterns{3};
category=category{1};

% numpres=5;
% % load original data
% datafile=fullfile('data',category, sprintf('%s_SNR%d_%dpres.mat',...
%     pattern,S2NR,numpres)); 
% load(datafile)

numpres=300;
% path to simulation results
dir=fullfile('simulations',category,sprintf('%s_SNR%d_%dpres', ...
        pattern,S2NR,numpres)); 

% ------------------------------------------------------------------------
% PLOT WEIGHTS -- Beta Mix
% ------------------------------------------------------------------------
format='pdf';
trainortest='training';
delayfunction='Beta-Mixture';
delaywin=300;
numdistributions=25;
% define file to load
filename=fullfile(dir,sprintf('%s-%s-%idelay-%idists_%s',trainortest,delayfunction, ...
    delaywin, numdistributions, files2parse{1}));

% import weights data
 data = import_weights(filename);

% calculate beta mixture across inputs
[betamix, ~] = calc_Betamix(data);

savepicshere=fullfile(dir,sprintf('%s-%s-%idelay-%idists_weights',trainortest,delayfunction, ...
    delaywin, numdistributions));
delaywin=0.2;           % delay window in seconds
% beta graphics
graphics_Betamix(betamix,savepicshere,delaywin,SGdata{2},format);

% ------------------------------------------------------------------------
% PLOT POTENTIAL
% ------------------------------------------------------------------------
delaywin=15;
savepicshere=fullfile(dir,sprintf('%s-%s-%idelay-%idists_potential',trainortest,delayfunction, ...
    delaywin, numdistributions));
format='pdf';
% define file to load
filename=fullfile(dir,sprintf('%s-%s-%idelay-%idists_%s',trainortest,delayfunction, ...
    delaywin, numdistributions, files2parse{2}));

% Number of presentations
numpres=5;


% Duration of Stimulus
stimduration=nnz(stimtimes)/numpres;


% import potential data
data = import_potential(filename,1, inf);

% presinwin=10;
% % potential graphics
% graphics_potential(data, ts,stimtimes,stimduration, savepicshere,format,presinwin);

% ------------------------------------------------------------------------
% PLOT WEIGHTS -- Mesq
% ------------------------------------------------------------------------
savepicshere=fullfile(dir,'weights');
format='pdf';
% define file to load
filename=fullfile(dir,files2parse{3});

% import weights data
data = import_weights(filename);

% calculate mesequilier weights across inputs
[mweights,~] = calc_Mesqweights(data);
delaywin=0.07;           % delay window in seconds

% mesq graphics
graphics_Mesq(meights,savepicshere,delaywin,F,format);

