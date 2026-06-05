%% computeSG(stream,fs,w,nfft,TW,TS)
% -----------------------------------------------------------------------
function [S,F,T]=calc_SG(stream,fs,w,nfft,TW,TS,isspeech)
% define vars
Nw = round(fs*TW*0.001);
Ns = round(fs*TS*0.001);
% obtain window function handle from string input
if isstr(w)
    w = str2func(w);
end;
% pre-emphasis filter for speech
if isspeech == true
    stream = filter([1 -0.95],1,stream);
end
% Spectrogram Analysis
[S,F,T] = spectrogram(stream,w(Nw).',Nw-Ns,nfft,fs);
S = abs(S);         % compute magnitude spectrum
S = S/max(max(S));  % normalize magnitude spectrum
%S = 20*log10(S);    % compute power spectrum in dB