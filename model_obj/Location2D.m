classdef Location2D
    %LOCATION2D Indicates a cross section's location
    %   Detailed explanation goes here
    
    properties(GetAccess = 'public', SetAccess = 'protected')
        anchor_xy = [DimMillimeter(0),DimMillimeter(0)];   %Distance from 
        %global origin xy coordinate to component's origin xy coordinate
        
        theta = DimRadian(0);  %Angles about global xy axes to 
                                     %rotate component's xy axes in radians
        R; %Rotation transformation matrix
    end
    
    methods
        function obj = Location2D(varargin)
            obj = createProperties(obj,nargin,varargin);            
            validateattributes(obj.anchor_xy,{'DimLinear'}, {'size', [1,2]})
            validateattributes(obj.theta,{'DimAngular'},{'size', [1,1]})
            theta = obj.theta.toRadians();
            obj.R = [ cos(theta), -sin(theta); ...
                      sin(theta),  cos(theta) ];
        end
        
        function transCoords = transformCoords(obj, coords, addTheta)
            
            %This function takes in an nx2 array of coordinates of the form
            %[x,y] and returns rotated and translated coordinates. The
            %translation and rotation are described by obj.anchor_xy and
            %obj.theta. The optional "addTheta" argument adds an
            %additional angle of "addTheta" to the obj.theta attribute.
            
            validateattributes(coords, {'DimLinear'},{})
            
            if exist('addTheta','var')
                validateattributes(addTheta, {'DimAngular'}, {'size',[1,1]})
                addTheta = addTheta.toRadians() + obj.theta.toRadians();
                T = [ cos(addTheta), -sin(addTheta); ...
                      sin(addTheta),  cos(addTheta) ];
            else
                T = obj.R;
            end
               
            rotateCoords = transpose(T*coords');
            transCoords(:,1) = rotateCoords(:,1) + obj.anchor_xy(1);
            transCoords(:,2) = rotateCoords(:,2) + obj.anchor_xy(2);
        end
    
        function locObj = relative(obj, relLinear, relAngular)
            
        %This function takes in a relative linear (relLinear) and relative
        %angular (relAngular) displacement and returns a new location
        %object that has been displaced relatively to this location object
    
        validateattributes(relLinear, {'DimLinear'}, {'size',[1,2]})
        validateattributes(relAngular, {'DimAngular'}, {'size',[1,1]})
        
        anchor = obj.anchor_xy + relLinear;
        angle = obj.theta + relAngular;
        
        disp(class(anchor))
        disp(class(angle))
        
        locObj = Location2D('anchor_xy', anchor, ...
                                'theta', angle );
        
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

