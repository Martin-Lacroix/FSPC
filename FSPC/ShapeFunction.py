import numpy as np

# %% Isoparametric Shape Functions

class ShapeFunction(object):

    def __init__(self): self.N = list()
    def __getitem__(self,i): return self.N[i]

    # Map the reference space to the global space

    def getPosition(self,node,pos):

        result = float(0)
        for i,fun in enumerate(self.N): result += fun(pos)*node[i]
        return result

# %% Line Element Shape Functions

class Line(ShapeFunction):
    def __init__(self):

        N1 = lambda pos: (1-pos)/2
        N2 = lambda pos: (1+pos)/2
        self.N = [N1,N2]

    # Projection of a point in the reference space

    def projection(self,node,pos):

        A = [node[1]/2-node[0]/2]
        B = np.array(pos-(node[0]+node[1])/2)
        param = np.linalg.lstsq(np.transpose(A),B,rcond=-1)[0]
        dist = np.linalg.norm(self.getPosition(node,param)-pos)

        # Check if the projection is in the element

        if abs(param)>1.001: return param,np.inf
        else: return param,dist

# %% Triangle Element Shape Functions

class Triangle(ShapeFunction):
    def __init__(self):

        N1 = lambda pos: 1-pos[0]-pos[1]
        N2 = lambda pos: pos[0]
        N3 = lambda pos: pos[1]
        self.N = [N1,N2,N3]

    # Projection of a point in the reference space

    def projection(self,node,pos):

        B = np.array(pos-node[0])
        A = [node[1]-node[0],node[2]-node[0]]
        param = np.linalg.lstsq(np.transpose(A),B,rcond=-1)[0]
        dist = np.linalg.norm(self.getPosition(node,param)-pos)

        # Check if the projection is in the element

        if all(-0.001<param) and (sum(param)<1.001): return param,dist
        else: return param,np.inf

# %% Quadrangle Element Shape Function

class Quadrangle(ShapeFunction):
    def __init__(self):

        N1 = lambda pos: (1-pos[0])*(1-pos[1])/4
        N2 = lambda pos: (1+pos[0])*(1-pos[1])/4
        N3 = lambda pos: (1+pos[0])*(1+pos[1])/4
        N4 = lambda pos: (1-pos[0])*(1+pos[1])/4
        self.N = [N1,N2,N3,N4]

    # Projection of a point in the reference space

    def projection(self,node,pos):

        J = np.zeros((2,3))
        param = np.array([0,0],dtype=float)

        while True:
            
            x,y = param
            F = 4*(self.getPosition(node,param)-pos)
            J[0] = node[0]*(y-1)+node[1]*(1-y)+node[2]*(1+y)-node[3]*(1+y)
            J[1] = node[0]*(x-1)-node[1]*(1+x)+node[2]*(1+x)+node[3]*(1-x)
            res = np.linalg.lstsq(np.transpose(J),F,rcond=-1)[0]

            param = param-res
            if all(abs(res)<1e-12): break

        # Check if the projection is in the element

        dist = np.linalg.norm(self.getPosition(node,param)-pos)
        if any(abs(param)>1.001): return param,np.inf
        else: return param,dist
