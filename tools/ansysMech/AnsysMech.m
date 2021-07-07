classdef AnsysMech < ToolBase & DrawerBase
    %AnsysMech Encapsulation for the Ansys Mechanical FEA software
    %   TODO: add more description
    %   TODO: add more description
    %   TODO: add more description
    %   TODO: add more description
    
    properties (GetAccess = 'public', SetAccess = 'private')
        iCoMapdlUnit;  %Ansys server object
    end
    
    methods
        function obj = AnsysMech(varargin)
            obj = obj.createProps(nargin,varargin);            
            obj.validateProps();            
        end
        
        function obj = open(obj, scratch_path, job_name)
            
            %scratch_path is folder where ansys writes to as well as places
            %server key

            %This code starts up the server from matlab... it is not
            %working yet and the server must be started from the mechanical
            %apdl launcher with the -aas parameter specified under the
            %additional parameters section
            
            exec_path = '"C:\Program Files\ANSYS Inc\v190\ansys\bin\winx64\MAPDL.exe"';
            job_flag = sprintf('-j %s', job_name);
            misc_flags = ' -p aa_r -np 2 -lch -s read -l en-us -aas -t -d win32';
            dir_flag = sprintf('-dir "%s"', scratch_path);
            
            cmd_str = sprintf('%s %s %s %s', exec_path, dir_flag, job_flag, misc_flags);
            system(cmd_str); %start ansys in as a server (aaS) mode
            
            orb = initialize_orb(); %this function comes from ansys matlab toolbox
            load_ansys_aas; %aas stands for ansys as a server
            key_str = sprintf('%s\\aaS_MapdlId.txt', scratch_path);
            obj.iCoMapdlUnit = actmapdlserver(orb, key_str);
            
        end
        
        function close(obj)
            %this may still not work properly yet
            obj.iCoMapdlUnit.executeCommandToString('/EXIT,NOSAVE');
        end
        
        function reset(obj)
           obj.iCoMapdlUnit.executeCommandToString('FINISH');
           obj.iCoMapdlUnit.executeCommandToString('/CLEAR,NOSTART');
        end
        
        function preprocesser(obj)
            obj.iCoMapdlUnit.executeCommandToString('FINISH');
            obj.iCoMapdlUnit.executeCommandToString('/PREP7');
        end
        
        function [kp_num] = create_keypoint(obj, x,y,z)
            
            %creates a keypoint at x,y,z and returns the id of the keypoint
            %created as an integer. keypoints are numbered automatically

            cmd_str = sprintf('K,0,%f,%f,%f', x,y,z); %create APDL command string
    
            out_str = obj.iCoMapdlUnit.executeCommandToString(cmd_str); %returns java.lang.String object
            out_str = string(out_str);%conver to matlab string
            
            %extract keypoint number out of string and convert to int type
            t = strsplit(strip(out_str));
            kp_num = uint64(str2double(t(end))); 

        end

        function [tokenLine] = drawLine(obj, startxy, endxy)
            
            %DRAWLINE Draw a line in the current Ansys APDL document.
            %   drawLine([start_x, _y], [end_x, _y]) draws a line
  
            kp_start = obj.create_keypoint(startxy(1), startxy(2), 0);
            kp_end = obj.create_keypoint(endxy(1),   endxy(2), 0);
            
            kp_nums = [kp_start, kp_end];
    
            line_cmd = sprintf('LSTR,%d,%d',kp_nums(1), kp_nums(2));
            line_output = obj.iCoMapdlUnit.executeCommandToString(line_cmd);
            line_output = string(line_output);
            
%             tokenLine = [kp_nums, line_output];
            tokenLine = kp_nums(1);
            
        end
        
        function [tokenArc] = drawArc(obj, centerxy, startxy, endxy)
            %DRAWARC Draw an arc in the current Ansys APDL document.
            %   drawarc([center_x,_y], [start_x, _y], [end_x, _y])
            %       draws an arc

            p_center = obj.create_keypoint(centerxy(1), centerxy(2), 0);
            p_zero = obj.create_keypoint(startxy(1), startxy(2), 0);
            p_axis = obj.create_keypoint(centerxy(1), centerxy(2), 1);

            kp_nums = [p_center, p_zero, p_axis];

            v1 = [startxy - centerxy, 0];
            v2 = [endxy - centerxy, 0];

            c = cross(v1,v2);
            deg = sign(c(3))*atan2d(norm(c),dot(v1,v2));

            if deg <0
               deg = deg + 360; 
            end

            rad = norm(v1);

            arc_cmd = sprintf('CIRCLE,%d,%f,%d,%d,%f', p_center, rad, p_axis, p_zero, deg);
            arc_output = obj.iCoMapdlUnit.executeCommandToString(arc_cmd);
            arc_output = string(arc_output);  
            
%             tokenArc = [kp_nums, arc_output];
            tokenArc = kp_nums(1);
            
        end
        
        
        function [save_output] = save_IGES(obj, path)

            save_cmd = sprintf("IGESOUT,'%s','IGES',,1", path);
            save_output = obj.iCoMapdlUnit.executeCommandToString(save_cmd);
            save_output = string(save_output);

        end
        
        function select(obj)
            %SELECT Selects something from canvas (?)
            %    select()
            
            % TODO:
            % Implement this...
            %
            % This will need to take in arguments, or maybe
            % CrossSect objects which then store internally all their
            % lines and surfaces that need to be selected
        end
        
        function new = revolve(obj, name, material, center, axis, angle, token)
            %REVOLVE Revolve a cross-section along an arc    
            %new = revolve(obj, name, material, center, axis, angle)
            %   name   - name of the newly extruded component
            %   center - x,y coordinate of center point of rotation
            %   axis   - x,y coordinate on the axis of ration (negative reverses
            %             direction) (0, -1) to rotate clockwise about the y axis
            %   angle  - Angle of rotation (dimAngular) 
            
        end
        
        function new = prepareSection(obj, csToken)
            
            %TO DO: implement function if necessary            
            
        end
        
        function setDefaultLengthUnit(obj, userUnit, makeAppDefault)
            %SETDEFAULTLENGTHUNIT Set the default unit for length.
            %   setDefaultLengthUnit(userUnit, makeAppDefault)
            %       Sets the units for length. 

            %   userUnit can be one of these options:
            %       'kilometers'
            %       'meters'
            %       'centimeters'
            %       'millimeters'
            %		'microns'
            %		'miles'
            %		'yards'	
            %		'feet'
            %       'inches'
            %
            %   This is a wrapper for Document::setDefaultLengthUnit

            %TO DO: implement if necessary
            
        end
        
        function viewAll(obj)
            %TO DO: implement if necessary
        end
        
        
        function setVisibility(obj, visibility)
            %TO DO: implement if necessary
        end
    end
    
    methods(Access = protected)
         function validateProps(obj)
            %VALIDATE_PROPS Validate the properties of this component
             
            % Use the superclass method to validate the properties 
            validateProps@ToolBase(obj);   
            validateProps@DrawerBase(obj);
         end
                  
         function obj = createProps(obj, len, args)
             %CREATE_PROPS Add support for value pair constructor
             
             validateattributes(len, {'numeric'}, {'even'});
             for i = 1:2:len 
                 obj.(args{i}) = args{i+1};
             end
         end
     end
end