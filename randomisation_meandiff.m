function [m_diff pval n_x1 n_x2] = randomisation_meandiff(x1,x2,n)
% randomisation test, to test whether the mean of two samples differs
% the two samples are two groups, where we measure the same variable (e.g. height in males/females)
%
% x1,x2 - column arrays of the two samples, may be of different length
% n - number of iterations
% m_diff - difference btw the two means
% pval - p from randomisation test
% n_x1, n_x2 - sample sizes
%
% the two samples are pooled, then divided randomly according to original sample sizes, 
% mean difference is calculated in each iteration,
% the statistics of mean difference will result the p for experimental data

m_diff = nanmean(x1) - nanmean(x2);

x_all = [x1;x2];
n_x1 = size(x1,1);
n_x2 = size(x2,1);
m_diff_p = zeros(n,1);
for i = 1:n
    pe = randperm(size(x_all,1));
    x_all_p = x_all(pe,1);
    x1_p = x_all_p(1:n_x1);
    x2_p = x_all_p(n_x1+1:end);
    m_diff_p(i) = nanmean(x1_p) - nanmean(x2_p);
end
[fi mi] = ksdensity(m_diff_p,'function','cdf','npoints',200);
m_ext = max(x_all) - min(x_all);
if m_diff <= 0
    pval = interp1([-m_ext mi m_ext],[0 fi 1],m_diff);
else
    pval = 1 - interp1([-m_ext mi m_ext],[0 fi 1],m_diff);
end
%figure
%plot(mi,fi)

