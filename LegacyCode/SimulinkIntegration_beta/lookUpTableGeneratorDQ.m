%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%   lookUpTableGenerator:  the script takes the current and angle indices
%                          as inputs and gives lookup tables for flux and
%                          torque values.
%
%                          Number of Poles need not be defined as
%                          Angle_index represents the electrical angle of
%                          the rotor
% 
%  Specifications:  
%          angle_brkpts: vector containing electrical angle indices
%
%          Id_brkpts: vector containing d axis current indices
%
%          Iq_brkpts: vector containing q axis current indices                    
%
%          FEA_data: structure containing flux and torque information for
%                    every index of electrical angle.
%
%
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%% breakpoints of dq currents and electrical angle to be defined in ascending order
% indices must be defined as row vectors(1 x m)
Ibase = 15;%Define base value of current here

Id_brkpts=Id;
Iq_brkpts=Iq;
angle_brkpts=thetae;

nId = length(Id);
nIq = length(Iq);
n_angle = length(angle_brkpts);


total_attempts = length(Id)*length(Iq);%*length(angle)

data_points = nId*nIq*n_angle;

%represents all possible data points of d-axis flux
Fd_points = zeros(1,data_points);
Fq_points = zeros(1,data_points);
F0_points = zeros(1,data_points);

Torque_points = zeros(1,data_points);
%Force_x_points = zeros(1,data_points);
%Force_y_points = zeros(1,data_points);

for i=1:total_attempts
    
    field = strcat('Iteration',num2str(i));%i(iteration number) is same as attempt_count
    disp(field); 
    
    start_index = ((i-1)*length(angle_brkpts)+1);
    end_index = i*length(angle_brkpts);
    
    %code needs change here based on the winding: Torque producing
    %component goes here:
    Fd_points(1,start_index:end_index) = FEAdataDQ.(field).Flux_a_d;
    Fq_points(1,start_index:end_index) = FEAdataDQ.(field).Flux_a_q;
    
    % Torque Flux is being calculated from d and q flux linkages 
    Fd_points(1,start_index:end_index) = (FEAdataDQ.(field).Flux_a_d + FEAdataDQ.(field).Flux_b_d)/2;
    Fq_points(1,start_index:end_index) = (FEAdataDQ.(field).Flux_a_q + FEAdataDQ.(field).Flux_b_q)/2;
    
    %F0_points(start_index:end_index,1) = (FEAdataDQ.(field).Flux_a_0 + FEAdataDQ.(field).Flux_b_d)/2;

    Torque_points(1,start_index:end_index) = FEAdataDQ.(field).torque;    
    %Force_x_points(1,start_index:end_index) = FEAdataDQ.(field).Forcex;    
    %Force_y_points(1,start_index:end_index) = FEAdataDQ.(field).Forcey; 


end

disp('Data points captured for all possible combinations of currents and angles');



%% 1 D lookup table to 2D lookup table (column = angle, row = Id x Iq)
Fd_lookup = (reshape(Fd_points(1:end),[n_angle,nIq*nId]))';
Fq_lookup = (reshape(Fq_points(1:end),[n_angle,nIq*nId]))';
%F0_lookup = (reshape(F0_raw(1:end-1),[n_angle,nIq*nId]))';
Torque_lookup = (reshape(Torque_points(1:end),[n_angle,nIq*nId]))';

%Force_x_lookup = (reshape(Force_x_points(1:end),[n_angle,nIq*nId]))';
%Force_y_lookup = (reshape(Force_y_points(1:end),[n_angle,nIq*nId]))'; 

Fd_lookup = [Fd_lookup(:,end-1), Fd_lookup, Fd_lookup(:,2)];
Fq_lookup = [Fq_lookup(:,end-1), Fq_lookup, Fq_lookup(:,2)];
%F0_lookup = [F0_lookup(:,end-1), F0_lookup, F0_lookup(:,2)];
Torque_lookup = [Torque_lookup(:,end-1), Torque_lookup, Torque_lookup(:,2)];

%Force_x_lookup = [Force_x_lookup(:,end-1), Force_x_lookup, Force_x_lookup(:,2)];
%Force_y_lookup = [Force_y_lookup(:,end-1), Force_y_lookup, Force_y_lookup(:,2)];

angle_brkpts = [2*angle_brkpts(1)-angle_brkpts(2), angle_brkpts,2*angle_brkpts(end)-angle_brkpts(end-1)];

%% Reshape 2-D Look Up table to 3-D Look Up table (column = Iq, row = Id, Page = Angle)
lookup_table_size = [length(Iq_brkpts),length(Id_brkpts),length(angle_brkpts)];

Flux_d_of_IdIqTheta = reshape(Fd_lookup,lookup_table_size);
Flux_q_of_IdIqTheta = reshape(Fq_lookup,lookup_table_size);
%Flux_0_of_IdIqTheta = reshape(F0_LUT,LUT_Size);
Torque_of_IdIqTheta = reshape(Torque_lookup,lookup_table_size);

%Force_x_of_IdIqTheta = reshape(Force_x_lookup,lookup_table_size);
%Force_y_of_IdIqTheta = reshape(Force_y_lookup,lookup_table_size);


%%%%Create inverse lookup table for obtaining current from flux and electrical angle%%%

%% Resolution of Flux to Current Lookup Table
flux_resolution = 100;

%% Determine Max and Min Flux Range
FluxD_index = linspace(min(Flux_d_of_IdIqTheta(:)),max(Flux_d_of_IdIqTheta(:)),flux_resolution);
FluxQ_index = linspace(min(Flux_q_of_IdIqTheta(:)),max(Flux_q_of_IdIqTheta(:)),flux_resolution);

%% Inverse Lookup Table Generation using gridfit
%gridfit.m can be downloaded from MATLAB file exchange

[id_m,iq_m] = meshgrid(Id_brkpts,Iq_brkpts);

for page_index =1:length(angle_brkpts)
    
    id_fit = gridfit(Flux_d_of_IdIqTheta(:,:,page_index),Flux_q_of_IdIqTheta(:,:,page_index),id_m,FluxD_index,FluxQ_index);
    IdLookupTable(:,:,page_index) = id_fit';
    iq_fit = gridfit(Flux_d_of_IdIqTheta(:,:,page_index),Flux_q_of_IdIqTheta(:,:,page_index),iq_m,FluxD_index,FluxQ_index);
    IqLookupTable(:,:,page_index) = iq_fit';
    
end


