function [m_diff pval n] = randomise_paireddiff(var1,var2,iter)
	% randomisation test, for testing difference between two matched variables
	% test is performed by permutating the two variables within the pairs, and calculating mean difference in each iteration
    % p value is obtained from the mean difference distribution from permutated data
	%
    % original:
	% (c) Enrico Glerean 2013 - Brain and Mind Laboratory Aalto University http://becs.aalto.fi/bml/
    % modified for arrays
 
	if(iter<=0)
		warning('setting permutations to 1e4');
		iter=1e4;
	end

	% test of same size
	kk1=size(var1);
	kk2=size(var2);
	if(kk1(1) ~= kk2(1))	error('arrays are not of same size'); end
    n = sum(~isnan(var1),1);

    m_diff = nanmean(var1 - var2,1);
	
    m_diff_p = zeros(iter,1);
    for i = 1:iter
        pe = randi(2,size(var1,1),1);
        temp = [var1 var2];
        temp2 = temp(pe == 2,:);
        temp3 = temp2(:,1);
        temp2(:,1) = temp2(:,2);
        temp2(:,2) = temp3;
        temp(pe == 2,:) = temp2;
		m_diff_p(i) = nanmean(temp(:,1) - temp(:,2),1);
   	end
	[fi mi] = ksdensity(m_diff_p,'function','cdf','npoints',200);
	% extreme values
    m_max = max(var1) - min(var2);
    m_min = min(var1) - max(var2);
    pval_left = interp1([m_min mi m_max],[0 fi 1],m_diff);    % trick to avoid NaNs
	if m_diff < 0
        pval = pval_left;
    elseif m_diff >= 0
        pval = 1-pval_left;
    end
    figure
    %plot(mi,fi)
end
    

        
