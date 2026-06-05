projectpath 		= '/Users/shad/TDNN';
category    		= 'consonants';
trainedpatterns 	= {'g'};
testedpatterns		= {'f'};

S2NR 		= [1];
numiter 	= [1];
numpres		= [50 10];
delaywin 	= 300;
numdist 	= [10];

for tp = 1:numel(trainedpatterns)
	for tstp = 1:numel(testedpatterns)
		for sn = 1:numel(S2NR)
			for nd = 1:numel(numdist)
				for ni = 1:numel(numiter)
					for np = 1:numel(numpres)
						graphics_summary(projectpath,category,trainedpatterns{tp},testedpatterns{tstp},S2NR(sn),numiter(ni),numpres(np),delaywin,numdist(nd));
					end
				end
			end
		end
	end
end

