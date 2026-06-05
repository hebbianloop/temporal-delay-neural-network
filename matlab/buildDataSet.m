%% buildDataSet(pattern,category,numpres,S2NR)
%
% Build a data set for a single pattern from a particular category type
% with a specified number of presentations and signal to noise ratio.
%
% An inter stimulus interval of 0.05s is inserted between each
% presentation.  Poissonian noise (lambda=2) is overlaid on the time series
% signal
% ------------------------------------------------------------------------
function buildDataSet(pattern,category,numpres,S2NR,nfft,padlength)
% Default Arguments
%padlength=0.05;     % ISI between presentations in secs
tscale=1000;        % milliisecond time bin!
lambda=2;           % lambda for poisson distribution
w=@hamming;         % windowing function for fft
TW=5;               % frame width (ms)
TS=1;               % frame shift (ms)
datafile=fullfile('data',category); %save dataset here
% ------------------------------------------------------------------------
fprintf('📐 DataSet Build Parameters \n\n');
fprintf('    🔩 Timescale (ms)                       ::   %d', tscale);
fprintf('\n    🔩 Inter-Stimulus Interval              ::   %d', padlength);
fprintf('\n    🔩 Poisson Lambda (for added noise)     ::   %d', lambda);
fprintf('\n    🔩 FFT Frequency Bins                   ::   %d', nfft);
%fprintf('\n    🔩 Spectrogram threshold                ::   %d', threshold);
fprintf('\n\nAll data will be written to  -  %s\n',datafile);
% ------------------------------------------------------------------------
% Check if category is a speech signal for signal processing
if any(strcmp(category,{'consonants','vowels','syllables'}))
    fprintf('\n\n!! THIS IS A SPEECH SIGNAL !!\n\n');
    isspeech=true;
else
    isspeech=false;
end
% ------------------------------------------------------------------------
% WORK IN PROGRESS :::: CHECK IF PATTERN IS AN IMAGE
% -- convert to sound file, insert noise then convert back to spectrogram
%    ** function works but adds frequency domain noise...
if any(strcmp(category,{'simple-images','fun-images'}))
    if ~exist(fullfile(datafile,strcat(pattern,'.flac')),'file')
        fs=22050; sigl=0.2;
        signal=imagetosignal(fullfile(datafile,strcat(pattern,'.png')),fs,sigl);
        audiowrite(fullfile(datafile,strcat(pattern,'.flac')),signal,fs)
        fprintf('Converting Image to Sound File (.flac): \n');
        fprintf('  🔩 sampling frequency (Hz)   ::  %d\n',fs);
        fprintf('  🔩 signal length (s)         ::  %d\n',sigl);
        fprintf('  📂 signal written to         ::  %s\n',fullfile(datafile,strcat(pattern,'.flac')));
    else
        [signal,~]=audioread(fullfile(datafile,strcat(pattern,'.flac')));
    end
end
% ------------------------------------------------------------------------
% Generate Stimulus Stream
% TODO: add jittering
fprintf('\n\n ... Generating Stream ...\n');
[stream,fs,stimtimes]=generateStream(datafile,pattern,padlength,numpres,tscale);
% ------------------------------------------------------------------------
% Compute SG of Stimulus Stream
fprintf('\n\n ... Computing Power Spectrum Estimate Over Time ...\n');
[S,F,T]=calc_SG(stream,fs,w,nfft,TW,TS,isspeech);
            %S=im2bw(S,graythresh(S));
            %S = mat2gray(S,[-5 -15]);
            % h=fspecial('gaussian',[20,20],1);
            % test=imfilter(S, h');
            % test=test<-10;
            % test=S;
            % se = strel('diamond',5);
            % test= imclose(S,se);
% ------------------------------------------------------------------------
fprintf('\n\n ... Plotting Timeseries & Spectral Density ...\n');
fprintf('\n  📂 PDF written to         ::  %s\n\n',fullfile(datafile,sprintf('%s_SNR%d_%dpres.pdf',pattern,S2NR,numpres)));
%%% MAKE PLOT!
time = linspace(0,length(stream)/fs,length(stream));
figure('color',[1 1 1],'position',[0 0 2560 1389],'Visible','off');
subplot(2,1,1)
plot(time,stream);
title(sprintf('Category: %s    Pattern: %s    SNR: %d    NumPres:  %d',category,pattern,S2NR,numpres),'fontsize',48)
xlabel('time (s)', 'fontsize', 32); ylabel('Normalized Amplitude', 'fontsize', 32)
set(gca,'fontsize',38)
set(gca,'xlim',[0 T(end)])
subplot(2,1,2)
imagesc(T,F,S)
axis('xy');
axis([0 T(end)  0 fs/2]);
xlabel('time (s)', 'fontsize', 32); ylabel('Frequency (Hz)', 'fontsize', 32)
title(sprintf('Spectrogram, nfft: %d',nfft),'fontsize',48)
colormap hot
set(gca,'fontsize',38)
export_fig(fullfile(datafile,sprintf('%s_SNR%d_%dpres',pattern,S2NR,numpres)),'-pdf')
close
% ------------------------------------------------------------------------
if ~isnan(S2NR)
    fprintf('\n\n ... Adding Poisson Distributed Noise To Stream ...\n');
    % ------------------------------------------------------------------------
    % Add Noise to Stimulus Stream
    %[stream,noise]=generateStream_addnoise(stream,lambda,S2NR);
    % ------------------------------------------------------------------------
    % Compute Time x Frequency Power Spectrum
    [S,F,T]=calc_SG(stream,fs,w,nfft,TW,TS,isspeech);
    % Threshold to binary map using Otsu's method  which chooses the 
    % threshold to minimize the intraclass variance of the thresholded 
    % black and white pixels.
    threshold=graythresh(S);
    S=imbinarize(S,threshold);
    %%%
    % Additive Noise
    %%%
    SIG=numel(find(S));
    [SIZEX,SIZEY]=size(S);
    TOTAL=SIZEX*SIZEY;
    SIG=SIG/TOTAL;
    NoiseProb=SIG/S2NR;
    for k = 1:length(S(:));
        randomegg=rand(1);
        if ~S(k)
           if randomegg<NoiseProb
               S(k)=1;
           end
        end
    end
    %insert bit flip code here:
   
    % ------------------------------------------------------------------------
    %%% MAKE A PLOT
    fprintf('\n\n ... Appending Noisy Timeseries & Thresholded Spectral Density to Plot ...\n');
    fprintf('\n  📂 PDF written to         ::  %s\n',fullfile(datafile,sprintf('%s_SNR%d_%dpres.pdf',pattern,S2NR,numpres)));
        % TODO: FILTER LOW FREQ (figure out why this is an issue)
       % if any(strcmp(pattern,{'chevron-l','chevron-r','x'}))
        %    S(sum(S,2)>size(S,2)/1.01,:)=zeros(1,size(S,2));
        %end 
    figure('color',[1 1 1],'position',[0 0 2560 1389],'Visible','off');
    subplot(2,1,1)
    plot(time,stream);
    title(sprintf('Category: %s    Pattern: %s    SNR: %d    NumPres:  %d',category,pattern,S2NR,numpres),'fontsize',48)
    xlabel('time (s)', 'fontsize', 32); ylabel('Normalized Amplitude', 'fontsize', 32)
    set(gca,'fontsize',38)
    set(gca,'xlim',[0 T(end)])
    subplot(2,1,2)
    imagesc(T,F,S)
    axis('xy');
    axis([0 T(end)  0 fs/2]);
    xlabel('time (s)', 'fontsize', 32); ylabel('Frequency (Hz)', 'fontsize', 32)
    title(sprintf('Normalized Spectrogram - thresholded @ %s',num2str(threshold)),'fontsize',48)
    colormap hot
    set(gca,'fontsize',38)
    export_fig(fullfile(datafile,sprintf('%s_SNR%d_%dpres',pattern,S2NR,numpres)),'-pdf','-append')
    close
    % ------------------------------------------------------------------------
    % Set uniform time binning
    fprintf('\n\n ... Setting Uniform Time Binning ...\n');
    ts=timeseries(S,T);
    ts=setuniformtime(ts,'Interval',1/tscale);
    T = ts.Time';
    S = squeeze(ts.Data);
    % ------------------------------------------------------------------------
    % Generate DataSet of Examples
    fprintf('\n\n ... ✏️ Writing DataSet to *.input file\n\n')
    writeDataSet(pattern,datafile,S,F,S2NR,numpres,tscale)
    SGdata={S,F,T};
    % ------------------------------------------------------------------------
    % Save data files for later inspection
    fprintf('\n\n ... Saving stream, SGdata, ts and stimtimes to *.MAT file\n\n')
    %save(fullfile(datafile,sprintf('%s_SNR%d_%dpres.mat',pattern,S2NR,numpres)),'stream','noise','SGdata','ts','stimtimes')
    save(fullfile(datafile,sprintf('%s_SNR%d_%dpres.mat',pattern,S2NR,numpres)),'stream','SGdata','ts','stimtimes')
else
    % ------------------------------------------------------------------------
    % Threshold to binary map using Otsu's method  which chooses the 
    % threshold to minimize the intraclass variance of the thresholded 
    % black and white pixels.
    threshold=graythresh(S);
    S=imbinarize(S,threshold);
    % ------------------------------------------------------------------------
    %%% make plot of noiseless
    fprintf('\n\n ... Appending Timeseries & Thresholded Spectral Density to Plot ...\n');
    fprintf('\n  📂 PDF written to         ::  %s\n',fullfile(datafile,sprintf('%s_SNR%d_%dpres.pdf',pattern,S2NR,numpres)));    
    figure('color',[1 1 1],'position',[0 0 2560 1389],'Visible','off');
    subplot(2,1,1)
    plot(time,stream);
    title(sprintf('Category: %s    Pattern: %s    SNR: %d    NumPres:  %d',category,pattern,S2NR,numpres),'fontsize',48)
    xlabel('time (s)', 'fontsize', 32); ylabel('Normalized Amplitude', 'fontsize', 32)
    set(gca,'fontsize',38)
    set(gca,'xlim',[0 T(end)])
    subplot(2,1,2)
    imagesc(T,F,S)
    axis('xy');
    axis([0 T(end)  0 fs/2]);
    xlabel('time (s)', 'fontsize', 32); ylabel('Frequency (Hz)', 'fontsize', 32)
    title(sprintf('Normalized Spectrogram - thresholded @ %s',num2str(threshold)),'fontsize',48)
    colormap hot
    set(gca,'fontsize',38)
    export_fig(fullfile(datafile,sprintf('%s_SNR%d_%dpres',pattern,S2NR,numpres)),'-pdf','-append')
    close
    % ------------------------------------------------------------------------
    % Set uniform time binning
    fprintf('\n\n ... Setting Uniform Time Binning ...\n');
    ts=timeseries(S,T);
    ts=setuniformtime(ts,'Interval',1/tscale);
    T = ts.Time';
    S = squeeze(ts.Data);
    % ------------------------------------------------------------------------
    % Generate DataSet of Examples
    fprintf('\n\n ... ✏️ Writing DataSet to *.input file\n\n')
    writeDataSet(pattern,datafile,S,F,nan,numpres,tscale)
    % ------------------------------------------------------------------------
    % Save data files for later inspection
    SGdata={S,F,T};
    fprintf('\n\n ... Saving stream, SGdata, ts and stimtimes to *.MAT file\n\n')
    save(fullfile(datafile,sprintf('%s_SNR%d_%dpres.mat',pattern,S2NR,numpres)),'stream','SGdata','ts','stimtimes')
end
