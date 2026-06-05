function signal = invSG(sgram)
% Default Args
[row, column] = size(sgram);
signal = [];
% Take the ifft of each column of pixels and piece together the results.
for i = 1 : column
    spectrogramWindow = sgram(:, i);
    signalWindow = real(ifft(spectrogramWindow));
    signal = [signal; signalWindow];
end