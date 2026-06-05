function [mweights]=calc_Mesqweights(weights)

Tcmem=10;
Tcsyn=2.5;
constant=2.11653473596;
delaywin=delaywin*1000;     % default is 70ms from Mesq08

t=linspace(0,delaywin,100);
mweights=zeros(length(weights),length(t));

for g = 1:length(weights)
    for k = 1:length(t) 
    mweights(g,k)= weights(g) * constant * (exp(-t(k)/Tcmem) - exp(-t(k)/Tcsyn));
    end
end