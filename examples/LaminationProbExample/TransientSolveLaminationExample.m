clc
clear

n = 1:20; %number of laminations

timeStep = 0.5; %ms
elecFreq = 20; %Hz
elecPeriod = 1/elecFreq*1e3; %ms
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

    %% Set transient solver options and solve
    if n(j) == 1
        endTime = 200; %ms
    else
        endTime = 75; % ms
    end
    
    timeSettings = [0, timeStep, endTime];
    mn_d_setparameter(toolMn.doc, '', 'TimeSteps', ...
        sprintf('[%g %%ms, %g %%ms, %g %%ms]', timeSettings), ...
        get(toolMn.consts,'infoArrayParameter'));
    
    solData = invoke(toolMn.doc, 'solveTransient2d');

    %% Post-processing
    
    % get average iron ohmic loss: calculate average loss for each 
    % lamination and then sum losses of all laminations
    time = mn_getTimeInstants(toolMn.mn, 1, true);
    for i = 1:length(compLam)
        eOhmicLossesT = mn_readConductorOhmicLoss(toolMn.mn, ...
            toolMn.doc, compLam(i).name, 1);
        OhmicLosses(i) = mean(eOhmicLossesT(end-round(elecPeriod/timeStep):end,2));
    end
    TotalOhmicLosses = sum(OhmicLosses);
    
    % get By in region at tooth center as a function of time
    thePoints = [BXPoints' BYPoint*ones(size(BXPoints')) BZPoint*ones(size(BXPoints'))];
    
    fieldData = [];
    ByAll = [];
    ByAvg = [];
    
    for k = 1:length(time)
        fieldData{k} = mn_readFieldAtPoints(toolMn.mn, thePoints, ...
                                                'B', 1, time(k));
        ByAll(k,:) = fieldData{k}(:,2)'; %gather just the y direction data as a function of time
        ByAvg(k,:) = mean(fieldData{k}(:,2)); %average of y direction field near center
    end
    %Get coil current
    Current = mn_readCoilCurrent(toolMn.mn, toolMn.doc, coilName, 1);
    %determine By peak
%     Bypeak = max(abs(ByAvg));
    Bypeak = max(abs(ByAvg(end-round(elecPeriod/timeStep):end)));
    
    %% Save file and exit
    
    FileName = [pwd '\lam_number_',num2str(n(j)),'_tr.mn'];
    Doc=invoke(toolMn.mn, 'saveDocument', FileName);
    invoke(toolMn.mn, 'exit');
    
    %% Data to save
    
    solutionData(j).TotalOhmicLosses = TotalOhmicLosses;
    solutionData(j).Bypeak = Bypeak;
    solutionData(j).ByAvg = ByAvg;
    solutionData(j).time = time;
    solutionData(j).Current = Current(:,2);
    
end

save('solDataTransientM19.mat','solutionData');
