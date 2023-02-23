SetFactory("OpenCASCADE");
Mesh.Binary = 1;

// Make a Triangle-Meshed Circle

Macro Tri_Circle

    k[] = {}; s[] = {}; c[] = {};
    c[0] = newc; Circle(c[0]) = {x,y,0,R};
    k[0] = newcl; Curve Loop(k[0]) = {c[0]};
    s[0] = news; Plane Surface(s[0]) = {k[0]};
    Transfinite Line{c[]} = N;
    
Return

// Make a Quad-Meshed Circle