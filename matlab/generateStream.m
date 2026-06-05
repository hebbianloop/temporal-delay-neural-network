%% stream=generateStream(projectdirectory,pattern,padlength,numpres,tscale)
%   
%   Create a stimulus stream with specified amount of padding between each
%   presentation.
%
%   TODO:add jittering
%   
%   ex)
%   projectdirectory=~/Project
%   cd projectdirectory
%   phone='k'
%   category='vowel'
%   padlength=0.05 (in s)
%   numpres=25
%
%   stream=generateStream(projectdirectory,pattern,padlength,numpres,tscale)
%
%	TODO: ADD CAPABILITY FOR MULTIPLE PATTERN STREAMS
%			* take counterbalanced index as input
% ------------------------------------------------------------------------
function [stream,fs,stimtimes]=generateStream(dir,pattern,...
                                                padlength,numpres,tscale)

audiofile = fullfile(dir,sprintf('%s.flac',pattern));
[wv, fs] = audioread(audiofile);      % Each sample is 1/fs seconds long
padding = round(padlength/(1/fs));    % number of samples in padding

% Total length of stream
padwv=padarray(wv,padding,0,'both');  % add padding to front and back of wv
stream =[];padwv=padwv';              % init vars

% Convert length of padding and waveform to appropriate time scale
tpadl=round(padlength*tscale);
twvl=round((length(wv)*(1/fs))*tscale);

% How long is each segment?
slen=length(padwv);
tlen=slen*(1/fs);

% Convert timing vector of each segment to specified timing scale
stimtimes_template=logical(zeros(1,round(tlen*tscale)));
% Insert ones only at times of stimulus presentation
stimtimes_template(tpadl+1:end-tpadl)=true;

stimtimes=[];

% loop and concatenate stream and stimulus times vector
for k = 1:numpres
    stream = [stream padwv];          
    stimtimes = [stimtimes stimtimes_template];
end


