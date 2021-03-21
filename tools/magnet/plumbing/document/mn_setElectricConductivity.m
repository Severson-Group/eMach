function mn_setElectricConductivity(mn,material_name,conductivity)
% MN_SETELECTRICCONDUCTIVITY Sets electric conductivity to the material in
% the user defined database
%       mn:  reference to open MagNet project
%       material_name:  material name in the user defined database to which
%       conductivity is set
%       conductivity:  conductivity value in [S/m]

invoke(mn, 'processcommand','REDIM ArrayOfValues(0, 1)');
invoke(mn, 'processcommand','ArrayOfValues(0, 0)= 20');
invoke(mn, 'processcommand',['ArrayOfValues(0, 1)= ' ...
    num2str(conductivity) '']);
invoke(mn, 'processcommand', ...
    ['Call getUserMaterialDatabase().setElectricConductivity("' ...
    material_name '", ArrayOfValues, infoLinearIsotropicReal)']);

end