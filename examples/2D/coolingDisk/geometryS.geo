Include "../../toolbox_2D.geo";

N = 7;
M = 5;
y = 0.28;
R = 0.025;

// Make the Circle

x = 0.2;
Call Quad_Circle;
c1[] = c[];

x = 0.45;
Call Quad_Circle;
c2[] = c[];

x = 0.7;
Call Quad_Circle;
c3[] = c[];

// Physical Boundary

Physical Surface("Solid_1") = {18:22};
Physical Surface("Solid_2") = {40:44};
Physical Surface("Solid_3") = {62:66};
Physical Curve("FSInterface") = {c1[],c2[],c3[]};

Mesh 2;