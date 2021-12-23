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
%          Ix_brkpts: vector containing d axis current indices
%
%          Iy_brkpts: vector containing q axis current indices                    
%
%          FEA_data: structure containing flux and torque information for
%                    every index of electrical angle.
%
%
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%% breakpoints of xy currents and electrical angle to be defined in ascending order
% indices must be defined as row vectors(1 x m)

%Define base value of current here
Ibase = 15;

Ix_brkpts=Ix;
Iy_brkpts=Iy;
angle_brkpts=thetae;

nIx = length(Ix);
nIy = length(Iy);
n_angle = length(angle_brkpts);

total_attempts = length(Ix)*length(Iy);%*length(angle)

data_points = nIx*nIy*n_angle;

%represents all possible data points of x and y-axis flux
Fx_points = zeros(1,data_points);
Fy_points = zeros(1,data_points);
%F0_points = zeros(1,data_points);

%Torque_points = zeros(1,data_points);
Force_x_points = zeros(1,data_points);
Force_y_points = zeros(1,data_points);

for i=1:total_attempts
    
    field = strcat('Iteration',num2str(i));%i(iteration number) is same as attempt_count
    disp(field); 
    
    start_index = ((i-1)*length(angle_brkpts)+1);
    end_index = i*length(angle_brkpts);
    
    %code needs change here based on the winding: Torque producing
    %component goes here:
    Fx_points(1,start_index:end_index) = FEAdataXY.(field).Flux_a_x;
    Fy_points(1,start_index:end_index) = FEAdataXY.(field).Flux_a_y;
    
    % Torque Flux is being calculated from d and q flux linkages 
    Fx_points(1,start_index:end_index) = (FEAdataXY.(field).Flux_b_x - FEAdataXY.(field).Flux_a_x)/2;
    Fy_points(1,start_index:end_index) = (FEAdataXY.(field).Flux_b_y - FEAdataXY.(field).Flux_a_y)/2;
    
    %F0_points(start_index:end_index,1) = (FEAdataXY.(field).Flux_a_0 + FEAdataXY.(field).Flux_b_d)/2;

    %Torque_points(1,start_index:end_index) = FEAdataXY.(field).torque;    
    Force_x_points(1,start_index:end_index) = FEAdataXY.(field).Forcex;    
    Force_y_points(1,start_index:end_index) = FEAdataXY.(field).Forcey; 


end

disp('Data points captured for all possible combinations of currents and angles');



%% 1 D lookup table to 2D lookup table (column = angle, row = Id x Iq)
Fx_lookup = (reshape(Fx_points(1:end),[n_angle,nIy*nIx]))';
Fy_lookup = (reshape(Fy_points(1:end),[n_angle,nIy*nIx]))';
%F0_lookup = (reshape(F0_raw(1:end-1),[n_angle,nIq*nId]))';
%Torque_lookup = (reshape(Torque_points(1:end),[n_angle,nIy*nIx]))';

Force_x_lookup = (reshape(Force_x_points(1:end),[n_angle,nIy*nIx]))';
Force_y_lookup = (reshape(Force_y_points(1:end),[n_angle,nIy*nIx]))'; 

Fx_lookup = [Fx_lookup(:,end-1), Fx_lookup, Fx_lookup(:,2)];
Fy_lookup = [Fy_lookup(:,end-1), Fy_lookup, Fy_lookup(:,2)];
%F0_lookup = [F0_lookup(:,end-1), F0_lookup, F0_lookup(:,2)];
Torque_lookup = [Torque_lookup(:,end-1), Torque_lookup, Torque_lookup(:,2)];

Force_x_lookup = [Force_x_lookup(:,end-1), Force_x_lookup, Force_x_lookup(:,2)];
Force_y_lookup = [Force_y_lookup(:,end-1), Force_y_lookup, Force_y_lookup(:,2)];

angle_brkpts = [2*angle_brkpts(1)-angle_brkpts(2), angle_brkpts,2*angle_brkpts(end)-angle_brkpts(end-1)];

%% Reshape 2-D Look Up table to 3-D Look Up table (column = Iq, row = Id, Page = Angle)
lookup_table_size = [length(Iy_brkpts),length(Ix_brkpts),length(angle_brkpts)];

Flux_x_of_IxIyTheta = reshape(Fx_lookup,lookup_table_size);
Flux_y_of_IxIyTheta = reshape(Fy_lookup,lookup_table_size);
%Flux_0_of_IdIqTheta = reshape(F0_LUT,LUT_Size);
%Torque_of_IdIqTheta = reshape(Torque_lookup,lookup_table_size);

Force_x_of_IxIyTheta = reshape(Force_x_lookup,lookup_table_size);
Force_y_of_IxIyTheta = reshape(Force_y_lookup,lookup_table_size);


%%%%Create inverse lookup table for obtaining current from flux and electrical angle%%%

%% Resolution of Flux to Current Lookup Table
flux_resolution = 100;

%% Determine Max and Min Flux Range
FluxX_index = linspace(min(Flux_x_of_IxIyTheta(:)),max(Flux_x_of_IxIyTheta(:)),flux_resolution);
FluxY_index = linspace(min(Flux_y_of_IxIyTheta(:)),max(Flux_y_of_IxIyTheta(:)),flux_resolution);

%% Inverse Lookup Table Generation using gridfit
%gridfit.m can be downloaded from MATLAB file exchange

[ix_m,iy_m] = meshgrid(Ix_brkpts,Iy_brkpts);

for page_index =1:length(angle_brkpts)
    id_fit = gridfit(Flux_x_of_IxIyTheta(:,:,page_index),Flux_y_of_IxIyTheta(:,:,page_index),ix_m,FluxX_index,FluxY_index);
    IdLookupTable(:,:,page_index) = id_fit';
    iq_fit = gridfit(Flux_x_of_IxIyTheta(:,:,page_index),Flux_y_of_IxIyTheta(:,:,page_index),iy_m,FluxX_index,FluxY_index);
    IqLookupTable(:,:,page_index) = iq_fit';
end


