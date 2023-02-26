Include "../../toolbox_3D.geo";
SetFactory("OpenCASCADE");

RS = 0.0125;
HS = 0.014;
HF = 0.05;

A = Sqrt(3)/3;
U = (RS/2)*A;
R = RS*A;

N = 15;
M = 12;

x = 0;
y = 0;
z = 0.064;
R = 0.0125;
Call Quad_Sphere;

// Physical Surfaces

Physical Volume("Solid") = {v[]};
Physical Surface("FSInterface") = {63,68,73,76,79,80};

Mesh.Binary = 1;
Mesh 3;