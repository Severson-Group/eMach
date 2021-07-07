classdef Location3D
    %LOCATION3D Indicates a cross section's location
    %   Detailed explanation goes here
    
    properties(GetAccess = 'public', SetAccess = 'protected')
        anchor_xyz = [DimMillimeter(0),DimMillimeter(0),DimMillimeter(0)]; 
        %Distance from global origin xyz coordinate to component's origin 
        %xyz coordinate
        theta = DimRadian(0);   %Angles about global xyz axes to rotate
                                %component's xyz axes in radians  
        u = [0,0,1]; %vector about which to rotate component about
        R; %Rotation transformation matrix
        Ux; %internal use direction matrix 1
        UU; %internal use direction matrix 2
    end
    
    methods
        function obj = Location3D(varargin)
            obj = createProperties(obj,nargin,varargin);            
            validateattributes(obj.anchor_xyz,{'DimLinear'},{'size',[1,3]})
            validateattributes(obj.theta,{'DimAngular'}, {'size', [1,1]})
            validateattributes(obj.u,{'numeric'}, {'numel', 3})
            
            %create rotation matrix
            %first check make sure u is a unit vector
            u = obj.u/norm(obj.u);
            theta = obj.theta.toRadians();
            
            %obj.UU and obj.Ux are intermediate direction vector dependent
            %matrices. See wikipedia page for more details:
            %"https://en.wikipedia.org/wiki/Rotation_matrix#In_three_dimensions"
            
            obj.UU = [ u(1)^2,     u(1)*u(2),   u(1)*u(3); ...
                       u(1)*u(2),  u(2)^2,      u(2)*u(3); ...
                       u(1)*u(3),  u(2)*u(3),   u(3)^2 ];
               
            obj.Ux = [ 0,    -u(3),   u(2); ...
                       u(3),  0,     -u(1); ...
                      -u(2),  u(1),   0    ];
              
            %creating rotation matrix
            obj.R = cos(theta)*eye(3) + sin(theta)*obj.Ux + ...
                    (1-cos(theta))*obj.UU;
               
        end
        
        function transCoords = transformCoords(obj, coords, add_theta)
            
            %This function takes in an nx3 or nx2 array of coordinates of 
            %the form [x,y,z] or [x,y] and returns rotated and translated
            %coordinates. The rotations are performed about the axis obj.u.
            %Translation and rotation are described by obj.anchor_xy and
            %obj.theta. The optional "add_theta" argument adds an
            %additional angle of "add_theta" to the obj.theta attribute.
            
            if exist('add_theta','var')
                validateattributes(add_theta,{'DimAngular'},{'size',[1,1]})
                add_theta = add_theta.toRadians() + obj.theta.toRadians();
                
                T = cos(add_theta)*eye(3) + sin(add_theta)*obj.Ux + ...
                    (1-cos(add_theta))*obj.UU;
            else
                T = obj.R;
            end
            
            if size(coords,2) == 2
                coords = [coords, zeros(size(coords,1),1)];
            end
               
            rotateCoords = transpose(T*coords');
            transCoords = zeros(size(rotateCoords));
            transCoords(:,1) = rotateCoords(:,1) + obj.anchor_xyz(1);
            transCoords(:,2) = rotateCoords(:,2) + obj.anchor_xyz(2);
            transCoords(:,3) = rotateCoords(:,3) + obj.anchor_xyz(3);
            
        end
        
        
    end
    
     methods(Access = protected)
         function obj = createProperties(obj, len, args)
             validateattributes(len, {'numeric'}, {'even'});
             for i = 1:2:len 
                 obj.(args{i}) = args{i+1};
             end
         end
     end    
end

