Include "../../toolbox_2D.geo";

N = 1;
M = 10;

// Make the Square

x = 0;
L = 1;
H = 0.02;
y = 0.01;
Call Quad_Square;

// Physical Boundary

Physical Surface("Solid") = {6};
Physical Curve("FSInterface") = {3};
Physical Curve("Clamped") = {2,4};
Physical Curve("Bottom") = {1};

Mesh 2;