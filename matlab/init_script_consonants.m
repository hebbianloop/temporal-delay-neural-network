%% DataSet Creation Script
%  
%  This script creates a dataset for simple-image patterns: r/l chevron and x
% 
%	* 50 Presentations of each stimuli with superimposed noise at +/- 0,1,2,6,10,12 SNRs
%	* DataSet is written as a text file with the extension *.input
%	* Plots of DataSets are also generated
% -----------------------------------------------------------------------------
clear all

category='consonants';
%patterns={'b','C','d','f','g','h','J','k','l','m','n','p','r','s','t','v','w','y','z'};
%patterns={'t','k','g'}; %change in place of articulation and voicing
patterns={'g'}; %change in place of articulation and voicing
numpres=[1];
S2NRvec=[1];
nfft=128;
padlength=0.15;

%addpath(genpath('./export_fig'))

for k = 1:numel(numpres)
	for kk = 1:numel(S2NRvec)
		buildDataSets(category,patterns,numpres(k),nfft,S2NRvec(kk),padlength)
	end
end
