function [betamix,numbetas] = calc_Betamix(betadata)

x = linspace(0,1,100);
numbetas = (size(betadata,2)/2);
betamix = zeros(size(betadata,1),length(x));

for k = 1:size(betadata,1)
    for g = 1:length(x)
        val = 0;
        for h = 1:2:(numbetas*2)
            a = betadata(k,h);
            b = betadata(k,h+1);
            val = betafun(a,b,x(g)) + val;
        end  
        val = val/numbetas;
        betamix(k,g) = val;
    end
end


