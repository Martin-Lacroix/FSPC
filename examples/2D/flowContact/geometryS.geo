Include "../../toolbox_2D.geo";

d = 0.05;
N = 70;

// Make the Peigne

x = -1;
L = 0.6;
R = 0.25;
y = -0.125;

Call Tri_Peigne;
Rotate{{0,0,1},{0,0,0},Pi}{Duplicata{Surface{14};}};

// Make the Circle

x = 0;
R = 0.375;
y = 1.875;
Call Tri_Circle;

// Physical Boundary

Physical Surface("Ball") = {27};
Physical Surface("Wall") = {14,15};
Physical Curve("FSInterface") = {1:11,13:23,25};
Physical Curve("Master") = {1:11,13:23};
Physical Curve("Clamped") = {12,24};
Physical Curve("Slave") = {25};

// Compute Mesh Size

Field[1] = Distance;
Field[1].CurvesList = {1:11,13:23,25};

Field[2] = MathEval;
Field[2].F = Sprintf("%g+F1*0.2",d);
Background Field = 2;

Mesh.MeshSizeExtendFromBoundary = 0;
Mesh.RecombinationAlgorithm = 0;
Mesh.SubdivisionAlgorithm = 1;
Mesh.RecombineAll = 1;
Mesh.Algorithm = 6;

Mesh 2;
