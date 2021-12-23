function [d,q]  = park(alpha,beta,theta)

dq = [cos(theta) sin(theta); -sin(theta) cos(theta)]*[alpha beta]';

d = dq(1);
q = dq(2);

end
