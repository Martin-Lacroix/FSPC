Include "../../toolbox_2D.geo";

x = 0;
y = 0;
d = 0.1;

// Make the Square

L = 5;
H = 5;
Call Tri_Square;

L = 2;
H = 2;
Call Tri_Square;

BooleanDifference{Surface{6};Delete;}
{Surface{12};Delete;}

// Physicl Boundary

Physical Surface("Fluid") = {6};
Physical Curve("FSInterface") = {5:8};
Physical Curve("Wall") = {1:4};

// Fluid Mesh Size

Field[1] = Distance;
Field[1].CurvesList = {5:8};

Field[2] = MathEval;
Field[2].F = Sprintf("%g+F1*0.05",d);
Background Field = 2;

Mesh.MeshSizeExtendFromBoundary = 0;
Mesh 2;