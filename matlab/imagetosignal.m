%% imagetosignal(path,fs,flength)
%
function signal = imagetosignal(path,fs,flength)
    % Read in the image
    I = imread(path);
    if ndims(I) == 3
        I = rgb2gray(I);
    end
    % We copy the image to generate phase information
    I = [I; flipud(I(2:end-1,:))];
    %image = [image; flipud(image)];  
    % Resize image to acquire required length in time
    %  * * The final length in time is equal to row * column
    %      - thus we must resize the image so that the number "row" added 
    %        "column" times gives us the desired length.  the easiest way
    %        to do this is to take the square root and make the image a
    %        square.    
    lengthinsamples=flength/(1/fs);
    imgsize=round(sqrt(lengthinsamples));
    I = imresize(I, [imgsize imgsize]);          
    % Convert to black and white
    I=im2bw(I,graythresh(I));
    % Take the ifft of each column of pixels and piece together the results.
    signal = [];
    for i = 1 : imgsize
    	spectrogramWindow = I(:, i);
%         spectrogramWindow=padarray(spectrogramWindow,60,0,'both');
    	signalWindow = real(ifft(ifftshift(spectrogramWindow),[],'symmetric'));
    	signal = [signal; signalWindow];
    end
%         signal=sgolayfilt(signal,1,99);
        %signal=medfilt1(signal,2);
end