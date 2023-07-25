function [rho pval n] = randomise_corr(var1,var2,iter,type)
	% randomisation test, for testing correlation between two paired variables
	% test is performed by permutating the two variables and calculating correlation in each iteration
    % p value is obtained from the correlation coefficient distribution from permutated data
	%
    % original:
	% (c) Enrico Glerean 2013 - Brain and Mind Laboratory Aalto University http://becs.aalto.fi/bml/
    % modified for arrays
 
	if(iter<=0)
		warning('setting permutations to 1e5');
		iter=1e4;
	end

	% test of same size
	kk1=size(var1);
	kk2=size(var2);
	if(kk1(1) ~= kk2(1))	error('arrays are not of same size'); end
    n = sum(~isnan(var1),1);

    rho = corr(var1,var2,'type',type,'rows','pairwise');
	
    surro = zeros(iter,1);
    for i = 1:iter
		pe = randperm(size(var1,1));
		temp = var1(pe,1);
		surro(i) = corr(temp,var2,'type',type,'rows','pairwise');
   	end
	[fi xi] = ksdensity(surro,'function','cdf','npoints',200);
	pval_left = interp1([-1 xi 1],[0 fi 1],rho);    % trick to avoid NaNs
	if rho < 0
        pval = pval_left;
    elseif rho >= 0
        pval = 1-pval_left;
    end
end
    

        
