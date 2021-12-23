current_folder = pwd;

msg = sprintf('Proceed with Selecting the folder containing run data for Id and Iq variations only');
h = msgbox(msg);

zero_current_fea_folder = uigetdir;
cd(zero_current_fea_folder);

% Id = [-1.1 -1:0.2:1 1.1];
% Iq = [-1.1 -1:0.2:1 1.1];
% Ix=0;
% Iy=0;

noi=length(Ix)*length(Iy)*length(Id)*length(Iq); %no of iterations
nosteps = 360; %as defined in em_fea_config script

%Gives (nosteps+1) number of elements useful during interpolation adn LUT
%creation
thetae=0:360/nosteps:360;

FEAdataDQ = struct('Iteration1',[]);

for i=1:1:noi
    
    substr = '';
    iterate_string = strcat('Iteration',num2str(i));
    FEAdataDQ = setfield(FEAdataDQ,iterate_string,[])
    
    if i == 1
        substr='';
        filepartname = substr;
    else
        substr=strcat('attempts_',num2str(i));
        %filepartname = strcat(substr,num2str(i));
        
    end
    
    extractStudy = 'TranPMSM_flux_of_fem_coil.csv';
    filename=strcat('proj_1_',filepartname,extractStudy);
    
    if isfile(filename)
        opts = detectImportOptions(filename);
        opts.DataLines=[8 inf];
        opts.VariableNames={'TimeStep','flux_Ua','flux_Ub','flux_Va','flux_Vb','flux_Wa','flux_Wb'};
        opts.SelectedVariableNames={'flux_Ua','flux_Ub','flux_Va','flux_Vb','flux_Wa','flux_Wb'};
        t = readtable(filename,opts);
        
        FEAdataDQ.(iterate_string).('Flux_Ua')=(t.flux_Ua)';
        FEAdataDQ.(iterate_string).('Flux_Ub')=(t.flux_Ub)';
        FEAdataDQ.(iterate_string).('Flux_Va')=(t.flux_Va)';
        FEAdataDQ.(iterate_string).('Flux_Vb')=(t.flux_Vb)';
        FEAdataDQ.(iterate_string).('Flux_Wa')=(t.flux_Wa)';
        FEAdataDQ.(iterate_string).('Flux_Wb')=(t.flux_Wb)';
        FEAdataDQ.(iterate_string).('thetae')=thetae;
        
        %setfield
    else
        error(strcat('File ',filename,'Not Found'))
    end
    
    %%Extracting Torque Values
    extractStudy = 'TranPMSM_torque.csv';
    filename=strcat('proj_1_',filepartname,extractStudy);
    if isfile(filename)
        opts = detectImportOptions(filename);
        opts.DataLines=[8 inf];
        opts.VariableNames={'TimeStep','torque'};
        opts.SelectedVariableNames={'torque'};
        t = readtable(filename,opts);
        
        FEAdataDQ.(iterate_string).('torque')=transpose(t.torque);
    else
        error(strcat('File ',filename,'Not Found'))
    end
    
    %%Extracting Force Values
    
    %The section for force retrieval may be commented out
    extractStudy = 'TranPMSM_force.csv';
    filename=strcat('proj_1_',filepartname,extractStudy);
    if isfile(filename)
        opts = detectImportOptions(filename);
        opts.DataLines=[8 inf];
        opts.VariableNames={'TimeStep','Forcex','Forcey','Force0'};
        opts.SelectedVariableNames={'Forcex','Forcey'};
        t = readtable(filename,opts);
        
        FEAdataDQ.(iterate_string).('Forcex')=transpose(t.Forcex);
        FEAdataDQ.(iterate_string).('Forcey')=transpose(t.Forcey);
    else
        error(strcat('File ',filename,'Not Found'))
    end
    
    %arguments to the function must be passed in the order of original
    %iteration script
    %Obtain the order of indices of currents passed in original FEA iteration
    
    [nx,ny,nd,nq] = indexValueReturn(length(Ix),length(Iy),length(Id),length(Iq),i);

    FEAdataDQ.(iterate_string).('d_current')=Id(nd);
    FEAdataDQ.(iterate_string).('q_current')=Iq(nq);
    FEAdataDQ.(iterate_string).('x_current')=Ix(nx);
    FEAdataDQ.(iterate_string).('y_current')=Iy(ny);
    
    
end
    
cd(current_folder);
    
    
    
