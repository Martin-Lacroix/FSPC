Include "../../toolbox_2D.geo";

D = 0.3;
d = 0.01;
eps = 1e-3;
N = 100;
M = 5;

// Make the Tool

L = 0.5;
R = 0.02;
y = -D-R;
x = 0.82;
H = 0.155;

Call Tri_Tool;
Rotate{{0,0,1},{0,0,0},Pi}{Duplicata{Surface{10};}};
Translate{2*x,0,0}{Surface{11};}

// Make the Solid

H = 0.55;
L = 0.02;
y = eps-(D-H/2);
x = x-R-L/2-eps;
Call Quad_Square;

// Physical Boundary

Physical Surface("Solid") = {22};
Physical Surface("Tool") = {10,11};
Physical Curve("ToolSurf") = {1:16};
Physical Curve("FSInterface") = {17:20};

Mesh 2;