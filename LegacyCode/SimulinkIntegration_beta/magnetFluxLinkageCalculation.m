%noi=1; %no of iterations is only 1 as the data is being collected when all
%values of current is zero

msg = sprintf('Proceed with Selecting the folder containing coil flux linkage data due to rotor magnets only');
h = msgbox(msg);

nosteps = 360;%specify the number of steps of electrical angle rotation chosen
thetae=0:360/nosteps:360;

current_folder = pwd;

zero_current_fea_folder = uigetdir;

cd(zero_current_fea_folder);

magnetFEA = struct('coilFluxLinkage',[],'inducedemf',[]);

% Iterate_string = strcat('Iteration',num2str(i));
% FEAdata = setfield(FEAdata,Iterate_string,[])


extractStudy = 'TranPMSM_flux_of_fem_coil.csv';
filename=strcat('proj_1_',extractStudy);
    
if isfile(filename)
    
    opts = detectImportOptions(filename);
    opts.DataLines=[8 inf];
    opts.VariableNames={'TimeStep','flux_Ua','flux_Ub','flux_Va','flux_Vb','flux_Wa','flux_Wb'};
    opts.SelectedVariableNames={'flux_Ua','flux_Ub','flux_Va','flux_Vb','flux_Wa','flux_Wb'};
    t = readtable(filename,opts);

    magnetFEA.coilFluxLinkage.('Flux_Ua')=(t.flux_Ua)';
    magnetFEA.coilFluxLinkage.('Flux_Ub')=(t.flux_Ub)';
    magnetFEA.coilFluxLinkage.('Flux_Va')=(t.flux_Va)';
    magnetFEA.coilFluxLinkage.('Flux_Vb')=(t.flux_Vb)';
    magnetFEA.coilFluxLinkage.('Flux_Wa')=(t.flux_Wa)';
    magnetFEA.coilFluxLinkage.('Flux_Wb')=(t.flux_Wb)';
    magnetFEA.coilFluxLinkage.('thetae')=thetae;

  
else
    error(strcat('File ',filename,'Not Found'))
end
    
   
    
cd(current_folder);    
    
    
