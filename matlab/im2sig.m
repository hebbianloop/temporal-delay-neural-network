%% imagetosignal(path)
%
function I = im2sig(path,fs,length)
    % Read in the image
    I = imread(path);
    % Convert to b/w image
    if ndims(I) == 3;
        I = rgb2gray(I);
    end    
    I = imcomplement(I);
    % Resize Image
    hres=200; Fmin=1; Fmax=256;
    chunk_s=floor(hres/ (Fmax*Fmin) * fs/2) *2;
    I = imresize(I, [hres length*fs/chunk_s]);
    I = double(I);    
    % append zeros left and right
    offset=1;
    I = [zeros(hres, floor(offset*fs/chunk_s)) I];
    I = [I zeros(hres, size(I,2)-size(I,2))];
    % append zeros top and bottom
    I = [zeros(floor(chunk_s/2 - (chunk_s*Fmax/fs)), size(I,2)); I];
    I = [I; zeros((size(I,1) - size(I,1)), size(I,2))];
    get_whole = @(Y) [flipud(Y); conj(Y(2:end-1,:))];
    %%%% append window to filter %%%%
    I = ifft(get_whole(I));
%    I = reshape(I, 1, length/(1/fs))';
    window_fact = 0;
    window = hanning(size(I,1));
%    I = I .* (1 - window_fact + window_fact * window);   
end
