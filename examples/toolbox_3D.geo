Macro Reset_All

    k[] = {}; s[] = {};
    r[] = {}; v[] = {};
    p[] = {}; l[] = {}; c[] = {};

Return

// Make a Non-Meshed Sphere

Macro Hole_Sphere

    Call Reset_All;
    SetFactory("OpenCASCADE");

    s[0] = newreg; Sphere(s[0]) = {x,y,z,R};
    MeshSize{PointsOf{Surface{s[0]};}} = d;
    Delete{Volume{s[0]};}

Return

// Make a Triangle-Meshed Sphere

Macro Tri_Sphere

    Call Reset_All;
    SetFactory("OpenCASCADE");

    s[0] = newreg; Sphere(s[0]) = {x,y,z,R};
    MeshSize{PointsOf{Surface{s[0]};}} = d;

Return

// Make a Quad-Meshed Sphere

Macro Quad_Sphere

    Call Reset_All;
    SetFactory("Built-in");

    // Points List

    RR = (0.6*R)*Sqrt(3)/3;

    p[0] = newp; Point(p[0]) = {x,y,z};
    p[1] = newp; Point(p[1]) = {x+RR,y+RR,z+RR};
    p[2] = newp; Point(p[2]) = {x+RR,y+RR,z-RR};
    p[3] = newp; Point(p[3]) = {x+RR,y-RR,z+RR};
    p[4] = newp; Point(p[4]) = {x+RR,y-RR,z-RR};
    p[5] = newp; Point(p[5]) = {x-RR,y+RR,z+RR};
    p[6] = newp; Point(p[6]) = {x-RR,y+RR,z-RR};
    p[7] = newp; Point(p[7]) = {x-RR,y-RR,z+RR};
    p[8] = newp; Point(p[8]) = {x-RR,y-RR,z-RR};

    RR = R*Sqrt(3)/3;

    p[9] = newp; Point(p[9]) = {x+RR,y+RR,z+RR};
    p[10] = newp; Point(p[10]) = {x+RR,y+RR,z-RR};
    p[11] = newp; Point(p[11]) = {x+RR,y-RR,z+RR};
    p[12] = newp; Point(p[12]) = {x+RR,y-RR,z-RR};
    p[13] = newp; Point(p[13]) = {x-RR,y+RR,z+RR};
    p[14] = newp; Point(p[14]) = {x-RR,y+RR,z-RR};
    p[15] = newp; Point(p[15]) = {x-RR,y-RR,z+RR};
    p[16] = newp; Point(p[16]) = {x-RR,y-RR,z-RR};

    // Line List

    l[0] = newl; Line(l[0]) = {p[1],p[2]};
    l[1] = newl; Line(l[1]) = {p[2],p[4]};
    l[2] = newl; Line(l[2]) = {p[3],p[4]};
    l[3] = newl; Line(l[3]) = {p[1],p[3]};
    l[4] = newl; Line(l[4]) = {p[1],p[5]};
    l[5] = newl; Line(l[5]) = {p[3],p[7]};
    l[6] = newl; Line(l[6]) = {p[4],p[8]};
    l[7] = newl; Line(l[7]) = {p[2],p[6]};
    l[8] = newl; Line(l[8]) = {p[5],p[6]};
    l[9] = newl; Line(l[9]) = {p[5],p[7]};

    l[10] = newl; Line(l[10]) = {p[7],p[8]};
    l[11] = newl; Line(l[11]) = {p[6],p[8]};
    l[12] = newl; Line(l[12]) = {p[1],p[9]};
    l[13] = newl; Line(l[13]) = {p[2],p[10]};
    l[14] = newl; Line(l[14]) = {p[3],p[11]};
    l[15] = newl; Line(l[15]) = {p[4],p[12]};
    l[16] = newl; Line(l[16]) = {p[5],p[13]};
    l[17] = newl; Line(l[17]) = {p[6],p[14]};
    l[18] = newl; Line(l[18]) = {p[7],p[15]};
    l[19] = newl; Line(l[19]) = {p[8],p[16]};

    // Circle List

    c[0] = newl; Circle(c[0]) = {p[9],p[0],p[10]};
    c[1] = newl; Circle(c[1]) = {p[10],p[0],p[12]};
    c[2] = newl; Circle(c[2]) = {p[11],p[0],p[12]};
    c[3] = newl; Circle(c[3]) = {p[9],p[0],p[11]};
    c[4] = newl; Circle(c[4]) = {p[9],p[0],p[13]};
    c[5] = newl; Circle(c[5]) = {p[11],p[0],p[15]};
    c[6] = newl; Circle(c[6]) = {p[12],p[0],p[16]};
    c[7] = newl; Circle(c[7]) = {p[10],p[0],p[14]};
    c[8] = newl; Circle(c[8]) = {p[13],p[0],p[14]};
    c[9] = newl; Circle(c[9]) = {p[13],p[0],p[15]};
    c[10] = newl; Circle(c[10]) = {p[15],p[0],p[16]};
    c[11] = newl; Circle(c[11]) = {p[14],p[0],p[16]};

    Transfinite Line{c[],l[0]:l[11]} = N;
    Transfinite Line{l[12]:l[19]} = Ceil(3*N/4);

    // Curve Loop

    k[0] = newcl; Curve Loop(k[0]) = {l[3],l[2],-l[1],-l[0]};
    k[1] = newcl; Curve Loop(k[1]) = {l[11],-l[10],-l[9],l[8]};
    k[2] = newcl; Curve Loop(k[2]) = {-l[6],-l[2],l[5],l[10]};
    k[3] = newcl; Curve Loop(k[3]) = {l[7],-l[8],-l[4],l[0]};
    k[4] = newcl; Curve Loop(k[4]) = {l[6],-l[11],-l[7],l[1]};
    k[5] = newcl; Curve Loop(k[5]) = {-l[5],-l[3],l[4],l[9]};
    k[6] = newcl; Curve Loop(k[6]) = {c[3],c[2],-c[1],-c[0]};
    k[7] = newcl; Curve Loop(k[7]) = {-l[2],l[14],c[2],-l[15]};
    k[8] = newcl; Curve Loop(k[8]) = {l[0],l[13],-c[0],-l[12]};
    k[9] = newcl; Curve Loop(k[9]) = {l[1],l[15],-c[1],-l[13]};

    k[10] = newcl; Curve Loop(k[10]) = {-l[3],l[12],c[3],-l[14]};
    k[11] = newcl; Curve Loop(k[11]) = {c[11],-c[10],-c[9],c[8]};
    k[12] = newcl; Curve Loop(k[12]) = {l[11],l[19],-c[11],-l[17]};
    k[13] = newcl; Curve Loop(k[13]) = {l[9],l[18],-c[9],-l[16]};
    k[14] = newcl; Curve Loop(k[14]) = {l[10],l[19],-c[10],-l[18]};
    k[15] = newcl; Curve Loop(k[15]) = {-l[8],l[16],c[8],-l[17]};
    k[16] = newcl; Curve Loop(k[16]) = {-c[6],-c[2],c[5],c[10]};
    k[17] = newcl; Curve Loop(k[17]) = {-l[6],l[15],c[6],-l[19]};
    k[18] = newcl; Curve Loop(k[18]) = {-l[5],l[14],c[5],-l[18]};
    k[19] = newcl; Curve Loop(k[19]) = {c[7],-c[8],-c[4],c[0]};
    k[20] = newcl; Curve Loop(k[20]) = {l[7],l[17],-c[7],-l[13]};
    k[21] = newcl; Curve Loop(k[21]) = {l[4],l[16],-c[4],-l[12]};
    k[22] = newcl; Curve Loop(k[22]) = {c[6],-c[11],-c[7],c[1]};
    k[23] = newcl; Curve Loop(k[23]) = {-c[5],-c[3],c[4],c[9]};

    // Surface Mesh

    For j In {0:23}

        s[j] = news; Surface(s[j]) = {k[j]};
        Transfinite Surface{s[j]};
        Recombine Surface{s[j]};

    EndFor

    // Volume Mesh

    r[0] = newsl; Surface Loop(r[0]) = {s[0]:s[5]};
    r[1] = newsl; Surface Loop(r[1]) = {s[0],s[6]:s[10]};
    r[2] = newsl; Surface Loop(r[2]) = {s[1],s[11]:s[15]};
    r[3] = newsl; Surface Loop(r[3]) = {s[2],s[7],s[14],s[16]:s[18]};
    r[4] = newsl; Surface Loop(r[4]) = {s[3],s[8],s[15],s[19]:s[21]};
    r[5] = newsl; Surface Loop(r[5]) = {s[5],s[10],s[13],s[18],s[21],s[23]};
    r[6] = newsl; Surface Loop(r[6]) = {s[4],s[9],s[12],s[17],s[20],s[22]};

    For j In {0:6}

        v[j] = newv; Volume(v[j]) = {r[j]};
        Transfinite Volume(v[j]);
        Recombine Volume(v[j]);

    EndFor
Return

// Make a Tri-Meshed Cylinder

Macro Tri_Cylinder

    Call Reset_All;
    SetFactory("OpenCASCADE");

    // Point list

    p[0] = newp; Point(p[0]) = {x,y,z,d};
    p[1] = newp; Point(p[1]) = {x+R,y,z,d};
    p[2] = newp; Point(p[2]) = {x-R,y,z,d};
    p[3] = newp; Point(p[3]) = {x,y+R,z,d};
    p[4] = newp; Point(p[4]) = {x,y-R,z,d};
    p[5] = newp; Point(p[5]) = {x,y,z+H,d};
    p[6] = newp; Point(p[6]) = {x+R,y,z+H,d};
    p[7] = newp; Point(p[7]) = {x-R,y,z+H,d};
    p[8] = newp; Point(p[8]) = {x,y+R,z+H,d};
    p[9] = newp; Point(p[9]) = {x,y-R,z+H,d};
    
    // Line List
    
    c[0] = newl; Circle(c[0]) = {p[2],p[0],p[4]};
    c[1] = newl; Circle(c[1]) = {p[4],p[0],p[1]};
    c[2] = newl; Circle(c[2]) = {p[1],p[0],p[3]};
    c[3] = newl; Circle(c[3]) = {p[3],p[0],p[2]};
    c[4] = newl; Circle(c[4]) = {p[7],p[5],p[9]};
    c[5] = newl; Circle(c[5]) = {p[9],p[5],p[6]};
    c[6] = newl; Circle(c[6]) = {p[6],p[5],p[8]};
    c[7] = newl; Circle(c[7]) = {p[8],p[5],p[7]};
    
    l[0] = newl; Line(l[0]) = {p[8],p[3]};
    l[1] = newl; Line(l[1]) = {p[6],p[1]};
    l[2] = newl; Line(l[2]) = {p[2],p[7]};
    l[3] = newl; Line(l[3]) = {p[9],p[4]};
    
    // Curve Loop
    
    k[0] = newcl; Curve Loop(k[0]) = {l[1],c[2],l[0],c[6]};
    k[1] = newcl; Curve Loop(k[1]) = {c[3],l[2],c[7],l[0]};
    k[2] = newcl; Curve Loop(k[2]) = {c[0],l[3],c[4],l[2]};
    k[3] = newcl; Curve Loop(k[3]) = {c[1],l[1],c[5],l[3]};
    k[4] = newcl; Curve Loop(k[4]) = {c[1],c[2],c[3],c[0]};
    k[5] = newcl; Curve Loop(k[5]) = {c[4],c[5],c[6],c[7]};
    
    // Surface Mesh
    
    s[0] = news; BSpline Surface(s[0]) = {k[0]};
    s[1] = news; BSpline Surface(s[1]) = {k[1]};
    s[2] = news; BSpline Surface(s[2]) = {k[2]};
    s[3] = news; BSpline Surface(s[3]) = {k[3]};
    s[4] = news; Plane Surface(s[4]) = {k[4]};
    s[5] = news; Plane Surface(s[5]) = {k[5]};

    // Mesh Generation
    
    r[0] = newsl; Surface Loop(r[0]) = {s[]};
    v[0] = newv; Volume(v[0]) = {r[0]};

Return
