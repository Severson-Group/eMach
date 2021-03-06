clc
clear

DRAW_MAGNET = 1;
DRAW_TIKZ   = 0;

%% Define cross sections

hollowCylinder1 = CrossSectHollowCylinder( ...
        'name', 'hollowCylinder1', ...
        'dim_t', DimMillimeter(4), ...
        'dim_r_o', DimMillimeter(80), ...
        'location', Location2D( ...
            'anchor_xy', DimMillimeter([0,0]), ...
            'theta', DimDegree(0).toRadians() ...
        ) ...
        );

%% Define components

cs = hollowCylinder1;

comp1 = Component( ...
        'name', 'comp1', ...
        'crossSections', cs, ...
        'material', MaterialGeneric('name', 'pm'), ...
        'makeSolid', MakeExtrude( ...
            'location', Location3D( ...
                'anchor_xyz', DimMillimeter([0,0,0]), ...
                'rotate_xyz', DimDegree([0,0,0]).toRadians() ...
                ), ...
            'dim_depth', DimMillimeter(80)) ...
        );

%% Draw via MagNet

if (DRAW_MAGNET)
    toolMn = MagNet();
    toolMn.open();
    toolMn.setVisibility(1);
    toolMn.setDefaultLengthUnit('DimMillimeter', false);

    comp1.make(toolMn, toolMn);

    toolMn.viewAll();
end

%% Draw via TikZ

if (DRAW_TIKZ)
    toolTikz = TikZ();
    toolTikz.open('output.txt');

    comp1.draw(toolTikz);

    toolTikz.close();
end
