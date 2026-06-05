%% beta = betafun(a,b,x)
%
% B(x) = [ gamma(a)+gamma(b) ] / gamma(a+b)
% Beta = 1/B(x) * (1-x)^(b-1) * x^(a-1)
% ------------------------------------------------------------------------
function [beta] = betafun(a,b,x)

betacoeff=exp(gammaln(a+b)-(gammaln(a)+gammaln(b)));
beta = ((1-x)^(b-1) * x^(a-1)) * betacoeff;

if x == 0 || x == 1
    beta=0;
end
if isnan(beta)
    beta=0;
end