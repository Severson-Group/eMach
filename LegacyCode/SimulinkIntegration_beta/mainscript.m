%%Define the currents for the Torque Lookup Iterations

Id = [-1.1 -1:0.2:1 1.1];
Iq = [-1.1 -1:0.2:1 1.1];
Ix = 0;
Iy = 0;

extractResultsFromCSV_DQ

%For transforming coil flux linkages into d and q flux linkage for coil groups 'a' and 'b'
FluxLinkages2DQ

lookUpTableGeneratorDQ

%% This section can be commented out for only torque lookUp table creation

%Define the currents for X and Y Force Lookup Iterations
Id = [0];
Iq = [1];
Ix = [-1.1 -1:0.2:1 1.1];
Iy = [-1.1 -1:0.2:1 1.1];

extractResultsFromCSV_XY

%For transforming coil flux linkages into x and y flux linkages for coil groups 'a' and 'b'
FluxLinkages2XY

lookUpTableGeneratorXY