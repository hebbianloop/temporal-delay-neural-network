%% generateStream_addnoise(stream,lambda,S2NR)
%
% Add Poissonian Noise to Stream
%------------------------------------------------------------------------
function [stream,noise] = generateStream_addnoise(stream,lambda,S2NR)
% Generate Poisson Noise Distribution
noise=poissrnd(lambda,size(stream));
% Scale Noise to Target (dB)
noise = ((noise / norm(noise)) * norm(stream)) / 10.0^(0.05*S2NR);
% Add Noise to Stream
stream=stream+noise;
