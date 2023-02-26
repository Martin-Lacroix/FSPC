Include "../../toolbox_3D.geo";
SetFactory("OpenCASCADE");

y = 0;
d = 2e-3;

// Make the Fluid

H = 0.4;
W = 0.25;
L = 0.35;
z = H/2;
x = L/2;

Call Tri_Square;

// Remove the Solid

H = 0.1;
W = 0.02;
L = 0.005;
x = 0.15+L/2;
z = H/2;

Call Tri_Square;
BooleanDifference{Volume{1};Delete;}{Volume{13};Delete;}

// New Structure Part

k = newcl; Curve Loop(k) = {13:16};
s = news; Plane Surface(s) = {k};
Reverse Surface{:};

// Physical Surface

Physical Volume("Fluid") = {1};
Physical Surface("Bottom") = {5,26};
Physical Surface("Polytope") = {7:11,26};
Physical Surface("FSInterface") = {7:11};
Physical Surface("Reservoir") = {2:4};
Physical Surface("Outlet") = {6};
Physical Surface("Inlet") = {1};

// Makes the Mesh

Field[1] = MathEval;
Field[1].F = "Max(0.002 + 0.1*(x-0.155),0)";
Field[2] = MathEval;
Field[2].F = "Max(0.002 + 0.1*(0.15-x),0)";
Field[3] = MathEval;
Field[3].F = "Max(0.002 + 0.1*(y-0.01),0)";
Field[4] = MathEval;
Field[4].F = "Max(0.002 - 0.1*(0.01+y),0)";
Field[5] = MathEval;
Field[5].F = "Max(0.002 + 0.1*(z-0.1),0)";

Field[6] = Max;
Field[6].FieldsList = {1,2,3,4,5};
Background Field = 6;

Mesh.MeshSizeExtendFromBoundary = 0;
Mesh.MeshSizeFromPoints = 0;
Mesh.Binary = 1;
Mesh 3;