function data=import_weights(filename)

delimiter = ',';
startRow = 3;

%% Determine how many columns
delimiter = ',';
fid = fopen(filename','rt');
for k = 1:startRow
    tlines = fgets(fid);
end
numcols = numel(strfind(tlines, delimiter)) + 1;
fclose(fid);


%% Build format specifier according to the number of columns
pattern = '%f';
formatSpec='';
for k = 1:numcols
    formatSpec = [formatSpec pattern];
end
formatSpec = [formatSpec '%[^\n\r]'];

%% Open the text file.
fileID = fopen(filename,'r');

%% Read columns of data according to format string.
% This call is based on the structure of the file used to generate this
% code. If an error occurs for a different file, try regenerating the code
% from the Import Tool.
dataArray = textscan(fileID, formatSpec, 'Delimiter', delimiter, 'HeaderLines' ,startRow-1, 'ReturnOnError', false);

% Delete last row (empty)
dataArray(end)=[];
dataArray(1:2)=[];
data=[];data=double(data);
for k = 1:length(dataArray)
    data(:,k)=dataArray{k};
end

%% Close the text file.
fclose(fileID);