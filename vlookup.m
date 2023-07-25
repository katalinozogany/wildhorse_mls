function output = vlookup(element,in_col,out_col,errortext)
% similar to excel vlookup function

if nargin < 4
    errortext = NaN;
end

s = size(element,1);

for i = 1:s
    row = find(ismember(in_col,element(i,1)));
    if size(row,1) > 0
        output(i,:) = out_col(row,:);
    else
        % when in_col does not contain the element
        output(i,1) = errortext;
    end
end