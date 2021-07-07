% Test of Location2D class

loc1 = Location2D( 'anchor_xy', [DimMillimeter(0), DimMillimeter(0)], ...
                   'theta', DimDegree(0) );

loc2 = Location2D( 'anchor_xy', [DimMillimeter(0), DimMillimeter(0)], ...
                   'theta', DimDegree(90) );
               
loc3 = Location2D( 'anchor_xy', [DimMillimeter(0), DimMillimeter(0)], ...
                   'theta', DimDegree(0) );
               
tol = 1e-5;
               
%% Test 1: transform coords 

x1 = DimMillimeter(1);
y1 = DimMillimeter(1);

coords = [x1, y1];
expected = [DimMillimeter(-1), DimMillimeter(1)];

transCoords = loc2.transformCoords(coords);

assert(strcmp( class(transCoords), class(expected) ));
assert( all( abs(double(expected) - double(transCoords)) < tol ) );


%% Test 2: relative method

relLocObj = loc1.relative( [DimMillimeter(1), DimMillimeter(1)], ...
                            DimDegree(90));
                        
expected = Location2D( 'anchor_xy', [DimMillimeter(1), DimMillimeter(1)], ...
                       'theta', DimDegree(90) );
                   
                   
                   
                   
                   
                   