Include "../../toolbox_2D.geo";

d = 0.02;

// Make the Square

x = 0;
H = 5;
L = 2;
y = -0.125;

Call Tri_Square;
s1 = s[0];

// Make the Peigne

x = -1;
L = 0.6;
R = 0.25;
y = -0.125;

Call Tri_Peigne;
s3 = Rotate {{0,0,1},{0,0,0},Pi} {Duplicata{Surface{s[0]};}};
s2 = s[0];

// Make the Circle

x = 0;
R = 0.375;
y = 1.875;

Call Tri_Circle;
s4 = s[0];

// Remove the Solid

BooleanDifference{Surface{s1};Delete;}{Surface{s2};Delete;}
BooleanDifference{Surface{s1};Delete;}{Surface{s3};Delete;}
BooleanDifference{Surface{s1};Delete;}{Surface{s4};Delete;}

// Physical Boundary

Physical Surface("Fluid") = {6};
Physical Curve("FSInterface") = {1,3,5,7:22,24,26,28:30};
Physical Curve("Reservoir") = {2,6,23,27};
Physical Curve("Polytope") = {29,30};
Physical Curve("FreeSurface") = {4};
Physical Curve("Inlet") = {25};

// Fluid Mesh Size

Field[1] = Distance;
Field[1].CurvesList = {1,3,5,7:22,24,26,28:30};

Field[2] = MathEval;
Field[2].F = Sprintf("%g+F1*0.1",d);
Background Field = 2;

Mesh.MeshSizeExtendFromBoundary = 0;
Mesh.MeshSizeFromPoints = 0;
Mesh 2;