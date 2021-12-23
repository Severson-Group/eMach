function [alpha,beta]  = clarke(U,V,W,Cm)

Clarke = zeros(2,3);
m = 3;
for i = 1:m
    Clarke(:,i) = Cm*[cos(2*pi/m*(i - 1)); sin(2*pi/m*(i - 1))];
end

DQ = Clarke*[U; V; W];
alpha = DQ(1);
beta = DQ(2);

end