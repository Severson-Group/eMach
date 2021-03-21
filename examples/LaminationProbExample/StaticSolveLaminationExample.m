clc
clear

n = 1:20; %number of laminations

CoilCurrent = 8.5; %Amp

BXPoints = linspace(8,10,10); %X Coordinates to calculate fields at (mm)
BYPoint = 15;   %Y Coordinate to calculate fields at (mm)
BZPoint = 0;    %Z Coorindate to calculate fields at (mm)

for j = 1:length(n)
    
    %% Call the function to construct the model
    
    [toolMn, compLam, coilName] = ConstructLaminationExample(n(j));

    %% Set up the excitation
    mn_d_setparameter(toolMn.doc, coilName, 'WaveFormType', 'DC', ...
        get(toolMn.consts,'InfoStringParameter'));
    mn_d_setparameter(toolMn.doc, coilName, 'Current', CoilCurrent, ...
        get(toolMn.consts,'infoNumberParameter'));

    %% Solve static
       
    solData = invoke(toolMn.doc, 'solveStatic2d');

    %% Post-processing
       
    % get By in region at tooth center as a function of time
    thePoints = [BXPoints' BYPoint*ones(size(BXPoints')) BZPoint*ones(size(BXPoints'))];
        
    fieldData = mn_readFieldAtPoints(toolMn.mn, thePoints, ...
                                                'B', 1);
    ByAll(j,:) = fieldData(:,2)'; %gather just the y direction data
    ByAvg = mean(fieldData(:,2)); %average of y direction field near center

    %Get coil current
    Current = mn_readCoilCurrent(toolMn.mn, toolMn.doc, coilName, 1);
    
    %% Save file and exit
    
    FileName = [pwd '\lam_number_',num2str(n(j)),'_st.mn'];
    Doc=invoke(toolMn.mn, 'saveDocument', FileName);
    invoke(toolMn.mn, 'exit');
    
    %% Data to save
    
    solutionData(j).ByAvg = ByAvg;
    solutionData(j).Current = Current(2);
        
end

save('solDataStatic.mat','solutionData');
