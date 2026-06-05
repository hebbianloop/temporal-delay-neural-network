projectpath 		= '/Users/shad/TDNN';
category    		= 'fun-images';
trainedpatterns 	= {'shady'};
testedpatterns		= {'shady'};

S2NR 		= [NaN];
delaywin 	= 300;
numdist 	= [40];

numiter 	= [1 2];
numpres		= [1];

for tp = 1:numel(trainedpatterns)
	for tstp = 1:numel(testedpatterns)
		for sn = 1:numel(S2NR)
			for nd = 1:numel(numdist)
				for ni = 1:numel(numiter)
					graphics_summary(projectpath,category,trainedpatterns{tp},testedpatterns{tstp},S2NR(sn),numiter(ni),numpres,delaywin,numdist(nd));
				end
			end
		end
	end
end

