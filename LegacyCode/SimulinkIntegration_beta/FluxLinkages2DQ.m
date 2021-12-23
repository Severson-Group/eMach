nosteps = length(FEAdataDQ.Iteration1.thetae);

flux_ad=zeros(1,nosteps);
flux_aq=zeros(1,nosteps);
flux_bd=zeros(1,nosteps);
flux_bq=zeros(1,nosteps);

total_attempts = length(Ix)*length(Iy)*length(Id)*length(Iq);

if(total_attempts > length(Id)*length(Iq))
    warning('Script not configured to handle more than two iterating inputs simultaneously');
    newline();
    warning('Results may be undesirable.......');
end

for i=1:total_attempts
    
    iterate_string = strcat('Iteration',num2str(i));

    for j = 1:1:nosteps

    [flux_a_alpha, flux_a_beta] = clarke(FEAdataDQ.(iterate_string).Flux_Ua(j),FEAdataDQ.(iterate_string).Flux_Va(j),FEAdataDQ.(iterate_string).Flux_Wa(j),2/3);
    [flux_a_d,flux_a_q] = park(flux_a_alpha, flux_a_beta, FEAdataDQ.(iterate_string).thetae(j)*pi/180);

    [flux_b_alpha, flux_b_beta] = clarke(FEAdataDQ.(iterate_string).Flux_Ub(j),FEAdataDQ.(iterate_string).Flux_Vb(j),FEAdataDQ.(iterate_string).Flux_Wb(j),2/3);
    [flux_b_d,flux_b_q] = park(flux_b_alpha, flux_b_beta, FEAdataDQ.(iterate_string).thetae(j)*pi/180);

    flux_ad(j)=flux_a_d;
    flux_aq(j)=flux_a_q;

    flux_bd(j)=flux_b_d;
    flux_bq(j)=flux_b_q;

    end

FEAdataDQ.(iterate_string).Flux_a_d = flux_ad;
FEAdataDQ.(iterate_string).Flux_a_q = flux_aq;

FEAdataDQ.(iterate_string).Flux_b_d = flux_bd;
FEAdataDQ.(iterate_string).Flux_b_q = flux_bq;

end

