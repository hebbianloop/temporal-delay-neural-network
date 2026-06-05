function y=smoothRows(x,windSize,normal)
%SMOOTHROWS - Smooths out data using a moving window. User specifies the
%   input data, window size and smoothing type.
% 
% FUNCTION:
%   smoothData = smoothRows(originalData, windowSize, smoothType)
%
% INPUT ARGS:
%   originalData    % the data you want to smooth out
%   windowSize      % size of desired smoothing window in samples (default is 40)
%   smoothType      % method in which to smooth data (default is standard boxcar method, true = normal distribution method)
%   
% OUTPUT ARGS:
%   smoothData      % the smoothed-out data

if ~exist('windSize','var')
    windSize=40; %80 ms window if sampling rate = 500 Hz
end

if ~exist('normal','var')
    normal=false;
end

if normal==true
    wind=normpdf(linspace(-2.5,2.5,windSize));
else
    wind=ones(1,windSize);
end

wind=wind./sum(windSize);

if 0
  y=convn(x,wind,'same');
else
  x2=[fliplr(x) x x];
  y=convn(x2,wind,'same');
  y=y(:,(size(x,2)+1):(end-size(x,2)));
end

