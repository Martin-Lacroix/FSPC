Include "../../toolbox_2D.geo";

d = 0.01;

// Make the Square

x = 0;
L = 1;
H = 0.2;
y = 0.1;
Call Tri_Square;

// Physical Boundary

Physical Surface("Fluid") = {6};
Physical Curve("FSInterface") = {3};
Physical Curve("Wall") = {1,2,4};

Mesh 2;