%% buildDataSets(category,patterns,numpres)
%
%  Generate a set of datasets for different stimuli/SNRs
%
%	Will build with the following Signal to Noise Ratios:
%		+/- 12,10,6,2,1,0,nan
% ------------------------------------------------------------------------
function buildDataSets(category,patterns,numpres,nfft,S2NRvec,padlength)

fprintf('🚩 Building Data Sets ::  %s\n\n',category);
for p = 1:numel(patterns)
    for snrs = 1:numel(S2NRvec)
    	fprintf('\n\n📌 Pattern           ::  %s',patterns{p});
    	fprintf('\n📌 Signal To Noise   ::  %d\n\n',S2NRvec(snrs));
        buildDataSet(patterns{p},category,numpres,S2NRvec(snrs),nfft,padlength)
    end
end
fprintf('\n\n✔️ DataSet Build Complete\n\n');