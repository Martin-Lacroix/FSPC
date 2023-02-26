Include "../../toolbox_3D.geo";
SetFactory("OpenCASCADE");

N = 15;
M = 12;

// Make the Sphere

x = 0;
y = 0;
z = 0.064;
R = 0.0125;
Call Quad_Sphere;

// Physical Surface

Physical Volume("Solid") = {v[]};
Physical Surface("FSInterface") = {63,68,73,76,79,80};

Mesh.Binary = 1;
Mesh 3;