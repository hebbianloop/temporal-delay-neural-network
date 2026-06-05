%% generateDataSet(phone,dir,data,inputs,SN2R)
%  ------------------------------------------------------------------------
function writeDataSet(phone,dir,data,inputs,SN2R,numpres,tscale)
if size(data,1) ~= numel(inputs)
    error('TDNN:generateDataSet:dimError','Number of input labels does not match data dimensions')
end
% Open File
fID = fopen(fullfile(dir,sprintf('%s_SNR%d_%dpres.input',phone,SN2R,numpres)),'w'); 
% Edit Header
    fprintf(fID,sprintf('@dataset %s_SNR%d_%dpres',phone,SN2R));
    fprintf(fID,sprintf('\n\n'));
    fprintf(fID,sprintf('@speed %d\n',(1/tscale)*1000));
% Edit Attributes    
for k = 1:numel(inputs)
    fprintf(fID,sprintf('@attribute input %.3fHz boolean\n',inputs(k)));
end
% Add Examples
fprintf(fID,sprintf('\n@examples\n'));
for k = 1:size(data,2)
    fprintf(fID,[sprintf('%d ',data(:,k)),sprintf('\n')]); %print fs at each t
end 
% Close File
fclose(fID);