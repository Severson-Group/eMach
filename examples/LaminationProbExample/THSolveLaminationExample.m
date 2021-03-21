clc
clear

n = 1:20; %number of laminations

elecFreq = 20; %Hz
currentAmplitude = 8.5; %Amp

BXPoints = linspace(8,10,10); %X Coordinates to calculate fields at (mm)
BYPoint = 15;   %Y Coordinate to calculate fields at (mm)
BZPoint = 0;    %Z Coorindate to calculate fields at (mm)

for j = 1:length(n)
    
    %% Call the function to construct the model
    
    [toolMn, compLam, coilName] = ConstructLaminationExample(n(j));

    %% Set up the excitation
    mn_d_setparameter(toolMn.doc, coilName, 'WaveFormType', 'SIN', ...
        get(toolMn.consts,'InfoStringParameter'));
    mn_d_setparameter(toolMn.doc, coilName, 'WaveFormValues', ...
        sprintf('[0, %g, %g]', currentAmplitude, elecFreq), ...
        get(toolMn.consts,'InfoArrayParameter'));

    %% Solve time-harmonic
      
    solData = invoke(toolMn.doc, 'solveTimeHarmonic2d');

    %% Post-processing
    
    % get average iron ohmic loss: calculate average loss for each 
    % lamination and then sum losses of all laminations
    for i = 1:length(compLam)
        eOhmicLossesT = mn_readConductorOhmicLoss(toolMn.mn, ...
            toolMn.doc, compLam(i).name, 1);
        OhmicLosses(:,i) = eOhmicLossesT(:,2);
    end
    TotalOhmicLosses = sum(OhmicLosses);
    
    % get By in region at tooth center as a function of time
    thePoints = [BXPoints' BYPoint*ones(size(BXPoints')) BZPoint*ones(size(BXPoints'))];

    fieldData = mn_readFieldAtPoints(toolMn.mn, thePoints, ...
                                                '|B|', 1);
%     ByAll(j,:) = fieldData(:,2)'; %gather just the y direction data
    ByAvg = mean(fieldData); %average of y direction field near center
    
    %% Save file and exit
    
    FileName = [pwd '\lam_number_',num2str(n(j)),'_th.mn'];
    Doc=invoke(toolMn.mn, 'saveDocument', FileName);
    invoke(toolMn.mn, 'exit');
    
    %% Data to save
    
    solutionData(j).TotalOhmicLosses = TotalOhmicLosses;
    solutionData(j).ByAvg = ByAvg;
    
end

save('solDataTH.mat','solutionData');
