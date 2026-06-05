%% DataSet Creation Script
%  
%  This script creates a dataset for simple-image patterns: r/l chevron and x
% 
%	* 25 Presentations of each stimuli with superimposed noise at +/- 0,1,2,6,10,12 SNRs
%	* DataSet is written as a text file with the extension *.input
%	* Plots of DataSets are also generated
% -----------------------------------------------------------------------------
clear all

category='simple-images';
%patterns={'chevron-l','chevron-r','x'};
patterns={'x'};
numpres=[1];
nfft=256;
S2NRvec=[1];
padlength=.120;

for k = 1:numel(numpres)
		buildDataSets(category,patterns,numpres(k),nfft,S2NRvec,padlength)
end