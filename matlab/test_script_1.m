%% Generate Stimulus Stream for STDP Temporal Pattern Recognition
%  -----------------------------------------------------------------------
try 
    cd /Users/seldamat/Dropbox/Projects/Language/Dissertation/modeling/
catch
    cd ~/Dropbox/Projects/Language/Dissertation/modeling/
end
phone='k';
audiofile = sprintf('./consonants/%s.flac',phone);
[wv, fs] = audioread(audiofile);
% -------------------------------------------------------- Create a Stream
% Each sample is 1/22050 seconds long
% 50 ms Padding equals 1103 samples
padding = 1103;
numpres = 100;
% Total length of stream
% stream = zeros(1,(length(wv)*numpres)+(1103*2*numpres));
padwv=padarray(wv,padding,0,'both');
stream =[];padwv=padwv';
for k = 1:numpres
    stream = [stream padwv];
end
% -----------------------------------------------  Insert Noise Into Stream
% define poisson noise vector
lambda=2;
% define noise vector
noise = poissrnd(lambda,size(stream));
% desired SNR level (dB)
snr = -6;
% get mixture speech at a desired SNR level
stream = addnoise(stream, noise, snr);
%  -----------------------------------------------------------------------
%  Plot Stream Waveform & Spectrogram
time = linspace(0,length(stream)/fs,length(stream));
figure('color',[1 1 1],'position',[0 0 1440 800]); 
subplot(2,1,1)
plot(time,stream);
subplot(2,1,2)
xlabel('time (s)', 'fontsize', 32); ylabel('Normalized Amplitude', 'fontsize', 32)
%     T = [18 1];         % vector of frame width and frame shift
%     w = @hamming;       % analysis window handle
%     nfft = 1024;        % fft analysis length
%     Slim = [-60 0];    % vector of spectrogram limits
%     alpha = [1 1]; % pre-emphasis filter coefficients
%     cmap = 'parula';
%     cbar = 'true';
%     type = 'lp';
[h,specdata]=myspectrogram(stream,fs);
colormap parula
%  -----------------------------------------------------------------------
%  Threshold to binary map & insert noise
                threshold = -30;
T = specdata{1};
F = specdata{2};
S = specdata{3};
N = length(stream);

S=S>threshold;
    figure;imagesc(T,F,S)
     axis('xy');
     axis([0 N/fs  0 fs/2]);

ts = timeseries(S,T);     
ts1 = setuniformtime(ts,'Interval',0.01)
time=0:.010:length(stream)/fs;
ts1=resample(ts,time);

% Generate Table
fID = fopen(sprintf('%sSNR%d',phone,snr),'w');     
    fprintf(fID,sprintf('@dataset %s_SNR%d',phone,snr));
    fprintf(fID,sprintf('\n\n'));
    fprintf(fID,sprintf('@speed 10\n'));
for k = 1:numel(F)
    fprintf(fID,sprintf('@attribute %.3fHz boolean\n',F(k)));
end
for k = 1:numel(T)
    fprintf(fID,[sprintf('%.3f',T(k)),sprintf('%d ',S(:,k)),sprintf('\n')]);
end 
fclose(fID);
     
% lambda=1;
% noise = poissrnd(lambda,size(S));
% 
% noisystream = logical(S+noise);
% % noisystream = noisystream > 0;
%     figure;imagesc(T,F,noisystream)
%      axis('xy');
%      axis([0 N/fs  0 fs/2]);

% % inline function for SNR calculation
% SNRdB = @(s,n)( 10*log10(sum(s(:).^2)/sum((n(:)-s(:)).^2)) ); 
% % define poisson noise vector
% lambda=2;
% % define noise vector
% noise = poissrnd(lambda,size(wv));
% % desired SNR level (dB)
% snr = 5;
% % get mixture speech at a desired SNR level
% noisy = addnoise( wv, noise, snr );
%     fprintf( ' Desired SNR: %0.2f dB\n', snr );
%     fprintf( 'Measured SNR: %0.2f dB\n', SNRdB(wv,noisy) );  
%  % generate time and frequency domain plots
%     hfig = figure( 'Position', [10 30 550 400], ... 
%         'PaperPositionMode', 'auto', 'Visible', 'on', 'color', 'w' ); 
%     % plot time domain waveforms
%     subplot( 2,1,1 ); hold on;
%     myspectrogram( wv, fs, [18 1], @hanning, 1024, [-60 -2] );
%     set( gca, 'ytick', [0:2000:fs/2], 'yticklabel', [0:2:round(0.5E-3*fs)] );
%     xlabel( 'Time (s)' );
%     ylabel( 'Frequency (kHz)' );
%     % plot spectral magnitude responses
%     subplot( 2,1,2 ); hold on;
%     myspectrogram( noisy, fs, [18 1], @hanning, 1024, [-60 -2] );
%     set( gca, 'ytick', [0:2000:fs/2], 'yticklabel', [0:2:round(0.5E-3*fs)] );
%     xlabel( 'Time (s)' );
    ylabel( 'Frequency (kHz)' );           
    
 % Generate a Poissonian Spike Train of Above Input
 % ------------------------------------------------------------
 
 % 1ms time bins
 % 450s long stream
 % Input occurs every 150s (with some jitter)
 
 