function [nI1,nI2,nI3,nI4] = indexValueReturn(n1,n2,n3,n4,counter)
% This function serves to return the index values for different loop
% variables when the code is run iteratively.

total_iterations=n1*n2*n3*n4;

if counter>total_iterations
    error('count number exceeds number of possible iterations')
end


nI1 = ceil(counter/(total_iterations/n1));
nI2 = ceil(counter/(total_iterations/(n1*n2)));
nI3 = ceil(counter/(total_iterations/(n1*n2*n3)));

if rem(counter,(total_iterations/(n1*n2*n3)))==0
    nI4 = n4;
else
    nI4 = rem(counter,(total_iterations/(n1*n2*n3)));
end

end

