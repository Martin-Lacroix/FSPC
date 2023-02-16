L = 0.9;
HF = 0.25;
HS = 0.03;
R = 0.025;

N = 7;
M = 5;

center = {0.2,0.45,0.7};
For j In {0:2}

    C = center[j];
    l = j*12;
    p = j*9;
    s = j*5;

    // Points List

    Point(1+p) = {C,HF+HS,0};
    Point(2+p) = {C,HF+HS-R,0};

    Point(3+p) = {C+R,HF+HS,0};
    Point(4+p) = {C,HF+HS+R,0};
    Point(5+p) = {C-R,HF+HS,0};

    Point(6+p) = {C,HF+HS-R/2,0};
    Point(7+p) = {C+R/2,HF+HS,0};
    Point(8+p) = {C,HF+HS+R/2,0};
    Point(9+p) = {C-R/2,HF+HS,0};

    // Lines List

    Circle(1+l) = {2+p,1+p,3+p};
    Circle(2+l) = {3+p,1+p,4+p};
    Circle(3+l) = {4+p,1+p,5+p};
    Circle(4+l) = {5+p,1+p,2+p};

    Line(5+l) = {6+p,7+p};
    Line(6+l) = {7+p,8+p};
    Line(7+l) = {8+p,9+p};
    Line(8+l) = {9+p,6+p};

    Line(9+l) = {6+p,2+p};
    Line(10+l) = {7+p,3+p};
    Line(11+l) = {8+p,4+p};
    Line(12+l) = {9+p,5+p};

    // Solid Surface

    Curve Loop(1+s) = {5+l,6+l,7+l,8+l};
    Curve Loop(2+s) = {9+l,1+l,-(10+l),-(5+l)};
    Curve Loop(3+s) = {10+l,2+l,-(11+l),-(6+l)};
    Curve Loop(4+s) = {11+l,3+l,-(12+l),-(7+l)};
    Curve Loop(5+s) = {12+l,4+l,-(9+l),-(8+l)};

    Plane Surface(1+s) = {1+s};
    Plane Surface(2+s) = {2+s};
    Plane Surface(3+s) = {3+s};
    Plane Surface(4+s) = {4+s};
    Plane Surface(5+s) = {5+s};

    Transfinite Line{1+l:8+l} = N;
    Transfinite Line{9+l:12+l} = M;

    Transfinite Surface{1+s};
    Transfinite Surface{2+s};
    Transfinite Surface{3+s};
    Transfinite Surface{4+s};
    Transfinite Surface{5+s};

EndFor

// Boundaries

Physical Surface("Solid_1") = {1,2,3,4,5};
Physical Surface("Solid_2") = {6,7,8,9,10};
Physical Surface("Solid_3") = {11,12,13,14,15};
Physical Curve("FSInterface") = {1,2,3,4,13,14,15,16,25,26,27,28};

Mesh.RecombineAll = 1;
Mesh.Algorithm = 8;
Mesh.Binary = 1;
Mesh 2;