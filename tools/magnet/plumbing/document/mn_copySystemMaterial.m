function mn_copySystemMaterial(mn,old_material_category,old_material,new_material)
% MN_COPYSYSTEMMATERIAL Copies system material and gives it a new name
%       mn:  reference to open MagNet project
%       old_material_category:  category to which old_material belongs, can
%       be found in MagNet, for example, for old_material = 'M-19 24 Ga':
%       old_material_category = 'Non-Oriented AISI Silicon Steel Materials'
%       
%       old_material:  system material name which the user wants to copy
%       new_material:  new material name to the copied material

% Check if there already exists material in the user defined database
% with the name 'new_material'
invoke(mn, 'processcommand', ...
    ['inDatabase = getUserMaterialDatabase().isMaterialInDatabase("' ...
    new_material '")']);
invoke(mn, 'processcommand', 'Call setVariant(0, inDatabase, "MATLAB")');
inDatabase = invoke(mn,  'getVariant', 0, 'MATLAB');

% If 'new_material' already exists, delete it
if inDatabase == 1
    invoke(mn, 'processcommand',...
        ['Call getUserMaterialDatabase().deleteMaterial("' ...
        new_material '")']);
end

% Copy system material
invoke(mn, 'processcommand', ...
    ['Call getUserMaterialDatabase().copySystemMaterial("' ...
    old_material_category '","' old_material '")']);

% Give a new name to the copied material
invoke(mn, 'processcommand', ...
    ['Call getUserMaterialDatabase().renameMaterial("' ...
    old_material '","' new_material '")']);

end