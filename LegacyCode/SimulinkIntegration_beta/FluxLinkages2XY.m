nosteps = length(FEAdataXY.Iteration1.thetae);

flux_ax=zeros(1,nosteps);
flux_ay=zeros(1,nosteps);
flux_bx=zeros(1,nosteps);
flux_by=zeros(1,nosteps);

total_attempts = length(Ix)*length(Iy)*length(Id)*length(Iq);

if(total_attempts > length(Ix)*length(Iy))
    warning('Script not configured to handle more than two iterating inputs simultaneously');
    newline();
    warning('Results may be undesirable.......');
end

for i=1:total_attempts
    
    iterate_string = strcat('Iteration',num2str(i));

    for j = 1:1:nosteps

    [flux_a_alpha, flux_a_beta] = clarke(FEAdata.(iterate_string).Flux_Ua(j),FEAdata.(iterate_string).Flux_Va(j),FEAdata.(iterate_string).Flux_Wa(j),2/3);
    [flux_a_x,flux_a_y] = park(flux_a_alpha, flux_a_beta, FEAdata.(iterate_string).thetae(j)*pi/180);

    [flux_b_alpha, flux_b_beta] = clarke(FEAdata.(iterate_string).Flux_Ub(j),FEAdata.(iterate_string).Flux_Vb(j),FEAdata.(iterate_string).Flux_Wb(j),2/3);
    [flux_b_x,flux_b_y] = park(flux_b_alpha, flux_b_beta, FEAdata.(iterate_string).thetae(j)*pi/180);

    flux_ax(j)=flux_a_x;
    flux_ay(j)=flux_a_y;

    flux_bx(j)=flux_b_x;
    flux_by(j)=flux_b_y;

    end

FEAdata.(iterate_string).Flux_a_x = flux_ax;
FEAdata.(iterate_string).Flux_a_y = flux_ay;

FEAdata.(iterate_string).Flux_b_x = flux_bx;
FEAdata.(iterate_string).Flux_b_y = flux_by;

end

