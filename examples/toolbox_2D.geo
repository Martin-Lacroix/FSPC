Macro Reset_All

    k[] = {}; s[] = {};
    p[] = {}; l[] = {}; c[] = {};

Return

// Make a Non-Meshed Circle

Macro Hole_Circle

    Call Reset_All;
    SetFactory("OpenCASCADE");

    c[0] = newl; Circle(c[0]) = {x,y,0,R};
    k[0] = newcl; Curve Loop(k[0]) = {c[0]};
    Transfinite Line{c[]} = N;
    
Return

// Make a Triangle-Meshed Circle

Macro Tri_Circle

    Call Reset_All;
    SetFactory("OpenCASCADE");
    
    c[0] = newl; Circle(c[0]) = {x,y,0,R};
    k[0] = newcl; Curve Loop(k[0]) = {c[0]};
    s[0] = news; Plane Surface(s[0]) = {k[0]};
    Transfinite Line{c[]} = N;
    
Return

// Make a Quad-Meshed Circle

Macro Quad_Circle

    RR = 0.6*R;
    Call Reset_All;
    SetFactory("OpenCASCADE");

    // Points List

    p[0] = newp; Point(p[0]) = {x,y,0};
    p[1] = newp; Point(p[1]) = {x,y-R,0};
    p[2] = newp; Point(p[2]) = {x+R,y,0};
    p[3] = newp; Point(p[3]) = {x,y+R,0};
    p[4] = newp; Point(p[4]) = {x-R,y,0};
    p[5] = newp; Point(p[5]) = {x,y-RR,0};
    p[6] = newp; Point(p[6]) = {x+RR,y,0};
    p[7] = newp; Point(p[7]) = {x,y+RR,0};
    p[8] = newp; Point(p[8]) = {x-RR,y,0};

    // Lines List

    c[0] = newl; Circle(c[0]) = {p[1],p[0],p[2]};
    c[1] = newl; Circle(c[1]) = {p[2],p[0],p[3]};
    c[2] = newl; Circle(c[2]) = {p[3],p[0],p[4]};
    c[3] = newl; Circle(c[3]) = {p[4],p[0],p[1]};

    l[0] = newl; Line(l[0]) = {p[5],p[6]};
    l[1] = newl; Line(l[1]) = {p[6],p[7]};
    l[2] = newl; Line(l[2]) = {p[7],p[8]};
    l[3] = newl; Line(l[3]) = {p[8],p[5]};
    l[4] = newl; Line(l[4]) = {p[5],p[1]};
    l[5] = newl; Line(l[5]) = {p[6],p[2]};
    l[6] = newl; Line(l[6]) = {p[7],p[3]};
    l[7] = newl; Line(l[7]) = {p[8],p[4]};

    // Surface List

    k[0] = newcl; Curve Loop(k[0]) = {l[0],l[1],l[2],l[3]};
    k[1] = newcl; Curve Loop(k[1]) = {l[4],c[0],l[5],l[0]};
    k[2] = newcl; Curve Loop(k[2]) = {l[5],c[1],l[6],l[1]};
    k[3] = newcl; Curve Loop(k[3]) = {l[6],c[2],l[7],l[2]};
    k[4] = newcl; Curve Loop(k[4]) = {l[7],c[3],l[4],l[3]};

    s[0] = news; Plane Surface(s[0]) = {k[0]};
    s[1] = news; Plane Surface(s[1]) = {k[1]};
    s[2] = news; Plane Surface(s[2]) = {k[2]};
    s[3] = news; Plane Surface(s[3]) = {k[3]};
    s[4] = news; Plane Surface(s[4]) = {k[4]};

    // Mesh Generation

    Transfinite Line{c[],l[0],l[1],l[2],l[3]} = N;
    Transfinite Line{l[4],l[5],l[6],l[7]} = Ceil(N/2);
    Transfinite Surface{s[]};
    Recombine Surface{s[]};

Return

// Make a Non-Meshed Square

Macro Hole_Square

    Call Reset_All;
    SetFactory("OpenCASCADE");

    // Points List

    p[0] = newp; Point(p[0]) = {x-L/2,y-H/2,0,d};
    p[1] = newp; Point(p[1]) = {x+L/2,y-H/2,0,d};
    p[2] = newp; Point(p[2]) = {x+L/2,y+H/2,0,d};
    p[3] = newp; Point(p[3]) = {x-L/2,y+H/2,0,d};

    // Lines List

    l[0] = newl; Line(l[0]) = {p[0],p[1]};
    l[1] = newl; Line(l[1]) = {p[1],p[2]};
    l[2] = newl; Line(l[2]) = {p[2],p[3]};
    l[3] = newl; Line(l[3]) = {p[3],p[0]};
    k[0] = newcl; Curve Loop(k[0]) = {l[]};
    
Return

// Make a Triangle-Meshed Square

Macro Tri_Square

    Call Reset_All;
    SetFactory("OpenCASCADE");

    // Points List

    p[0] = newp; Point(p[0]) = {x-L/2,y-H/2,0,d};
    p[1] = newp; Point(p[1]) = {x+L/2,y-H/2,0,d};
    p[2] = newp; Point(p[2]) = {x+L/2,y+H/2,0,d};
    p[3] = newp; Point(p[3]) = {x-L/2,y+H/2,0,d};

    // Lines List

    l[0] = newl; Line(l[0]) = {p[0],p[1]};
    l[1] = newl; Line(l[1]) = {p[1],p[2]};
    l[2] = newl; Line(l[2]) = {p[2],p[3]};
    l[3] = newl; Line(l[3]) = {p[3],p[0]};

    // Surface List

    k[0] = newcl; Curve Loop(k[0]) = {l[]};
    s[0] = news; Plane Surface(s[0]) = {k[0]};
    
Return

// Make a Quad-Meshed Square

Macro Quad_Square

    Call Reset_All;
    SetFactory("OpenCASCADE");

    // Points List

    p[0] = newp; Point(p[0]) = {x-L/2,y-H/2,0};
    p[1] = newp; Point(p[1]) = {x+L/2,y-H/2,0};
    p[2] = newp; Point(p[2]) = {x+L/2,y+H/2,0};
    p[3] = newp; Point(p[3]) = {x-L/2,y+H/2,0};

    // Lines List

    l[0] = newl; Line(l[0]) = {p[0],p[1]};
    l[1] = newl; Line(l[1]) = {p[1],p[2]};
    l[2] = newl; Line(l[2]) = {p[2],p[3]};
    l[3] = newl; Line(l[3]) = {p[3],p[0]};

    // Surface List

    k[0] = newcl; Curve Loop(k[0]) = {l[]};
    s[0] = news; Plane Surface(s[0]) = {k[0]};

    Transfinite Line{l[0],l[2]} = M;
    Transfinite Line{l[1],l[3]} = N;

    Transfinite Surface{s[]};
    Recombine Surface{s[]};
    
Return

// Make a Triangle-Meshed Trapez

Macro Tri_Trapez

    Call Reset_All;
    SetFactory("OpenCASCADE");

    // Points List

    p[0] = newp; Point(p[0]) = {x-L/2,y-H/2,0,d};
    p[1] = newp; Point(p[1]) = {x+L/2,y-H/2,0,d};
    p[2] = newp; Point(p[2]) = {x+W/2,y+H/2,0,d};
    p[3] = newp; Point(p[3]) = {x-W/2,y+H/2,0,d};

    // Lines List

    l[0] = newl; Line(l[0]) = {p[0],p[1]};
    l[1] = newl; Line(l[1]) = {p[1],p[2]};
    l[2] = newl; Line(l[2]) = {p[2],p[3]};
    l[3] = newl; Line(l[3]) = {p[3],p[0]};

    // Surface List

    k[0] = newcl; Curve Loop(k[0]) = {l[]};
    s[0] = news; Plane Surface(s[0]) = {k[0]};
    
Return

// Make a Triangle-Meshed Peigne

Macro Tri_Peigne

    LL = 5*L/6;
    Call Reset_All;
    SetFactory("OpenCASCADE");

    // Points List
    
    p[0] = newp; Point(p[0]) = {x,y-5*R,0,d};
    p[1] = newp; Point(p[1]) = {x,y+5*R,0,d};
    p[2] = newp; Point(p[2]) = {x+L,y+5*R,0,d};
    p[3] = newp; Point(p[3]) = {x+L,y+4*R,0,d};
    p[4] = newp; Point(p[4]) = {x+L,y+3*R,0,d};
    p[5] = newp; Point(p[5]) = {x+LL,y+3*R,0,d};
    p[6] = newp; Point(p[6]) = {x+LL,y+2*R,0,d};
    p[7] = newp; Point(p[7]) = {x+LL,y+R,0,d};
    p[8] = newp; Point(p[8]) = {x+L,y+R,0,d};
    p[9] = newp; Point(p[9]) = {x+L,y,0,d};

    p[10] = newp; Point(p[10]) = {x+L,y-R,0,d};
    p[11] = newp; Point(p[11]) = {x+LL,y-R,0,d};
    p[12] = newp; Point(p[12]) = {x+LL,y-2*R,0,d};
    p[13] = newp; Point(p[13]) = {x+LL,y-3*R,0,d};
    p[14] = newp; Point(p[14]) = {x+L,y-3*R,0,d};
    p[15] = newp; Point(p[15]) = {x+L,y-4*R,0,d};
    p[16] = newp; Point(p[16]) = {x+L,y-5*R,0,d};

    // Lines List

    c[0] = newl; Circle(c[0]) = {p[14],p[15],p[16]};
    c[1] = newl; Circle(c[1]) = {p[13],p[12],p[11]};
    c[2] = newl; Circle(c[2]) = {p[8],p[9],p[10]};
    c[3] = newl; Circle(c[3]) = {p[7],p[6],p[5]};
    c[4] = newl; Circle(c[4]) = {p[2],p[3],p[4]};

    l[0] = newl; Line(l[0]) = {p[0],p[16]};
    l[1] = newl; Line(l[1]) = {p[14],p[13]};
    l[2] = newl; Line(l[2]) = {p[11],p[10]};
    l[3] = newl; Line(l[3]) = {p[8],p[7]};
    l[4] = newl; Line(l[4]) = {p[5],p[4]};
    l[5] = newl; Line(l[5]) = {p[2],p[1]};
    l[6] = newl; Line(l[6]) = {p[1],p[0]};

    // Solid Surface

    k[0] = newcl; Curve Loop(k[0]) = {l[0],c[0],l[1],
    c[1],l[2],c[2],l[3],c[3],l[4],c[4],l[5],l[6]};
    s[0] = news; Plane Surface(s[0]) = {k[0]};

Return

// Make a Triangle-Meshed Door

Macro Tri_Tool

    Call Reset_All;
    SetFactory("OpenCASCADE");

    // Points List
    
    p[0] = newp; Point(p[0]) = {x-L,y-R,0,d};
    p[1] = newp; Point(p[1]) = {x+L,y-R,0,d};
    p[2] = newp; Point(p[2]) = {x+L,y+R,0,d};
    p[3] = newp; Point(p[3]) = {x+R,y+R,0,d};
    p[4] = newp; Point(p[4]) = {x+R,y+H+R,0,d};
    p[5] = newp; Point(p[5]) = {x,y+H+R,0,d};
    p[6] = newp; Point(p[6]) = {x-R,y+H+R,0,d};
    p[7] = newp; Point(p[7]) = {x-R,y+R,0,d};
    p[8] = newp; Point(p[8]) = {x-L,y+R,0,d};

    // Lines List

    l[0] = newl; Line(l[0]) = {p[0],p[1]};
    l[1] = newl; Line(l[1]) = {p[1],p[2]};
    l[2] = newl; Line(l[2]) = {p[2],p[3]};
    l[3] = newl; Line(l[3]) = {p[3],p[4]};
    l[5] = newl; Line(l[5]) = {p[6],p[7]};
    l[6] = newl; Line(l[6]) = {p[7],p[8]};
    l[7] = newl; Line(l[7]) = {p[8],p[0]};

    // Curve Loop

    l[4] = newl; Circle(l[4]) = {p[6],p[5],p[4]};
    k[0] = newcl; Curve Loop(k[0]) = {l[]};
    s[0] = news; Plane Surface(s[0]) = {k[0]};

Return
