import numpy as np

# %% Isoparametric Finite Element

class Element(object):

    def getPosition(self,node,pos):

        result = float(0)
        for i,N in enumerate(self.N): result += N(pos)*node[i]
        return result

# %% Linear Line Finite Element

class Line(Element):
    def __init__(self):
        
        self.N = list()
        self.N.append(lambda pos: (1-pos)/2)
        self.N.append(lambda pos: (1+pos)/2)

    # Distance between a point and the projection

    def distance(self,parm,node,pos):

        if abs(parm)>1.001: return np.inf
        return np.linalg.norm(self.getPosition(node,parm)-pos)

    # Projection of a point in the reference space

    def projection(self,node,pos):
    
        A = np.diff(node,axis=0)/2
        B = np.array(pos-np.sum(node,axis=0)/2)
        return np.linalg.lstsq(np.transpose(A),B,-1)[0]

# %% Linear Triangle Finite Element

class Triangle(Element):
    def __init__(self):

        self.N = list()
        self.N.append(lambda pos: 1-pos[0]-pos[1])
        self.N.append(lambda pos: pos[0])
        self.N.append(lambda pos: pos[1])

    # Distance between a point and the projection

    def distance(self,parm,node,pos):

        if any(-0.001>parm) or sum(parm)>1.001: return np.inf
        return np.linalg.norm(self.getPosition(node,parm)-pos)

    # Projection of a point in the reference space

    def projection(self,node,pos):

        B = np.array(pos-node[0])
        A = [node[1]-node[0],node[2]-node[0]]
        return np.linalg.lstsq(np.transpose(A),B,-1)[0]

# %% Linear Quadrangle Finite Element

class Quadrangle(Element):
    def __init__(self):

        self.N = list()
        self.N.append(lambda pos: (1-pos[0])*(1-pos[1])/4)
        self.N.append(lambda pos: (1+pos[0])*(1-pos[1])/4)
        self.N.append(lambda pos: (1+pos[0])*(1+pos[1])/4)
        self.N.append(lambda pos: (1-pos[0])*(1+pos[1])/4)

    # Distance between a point and the projection

    def distance(self,parm,node,pos):

        if any(abs(parm)>1.001): return np.inf
        return np.linalg.norm(self.getPosition(node,parm)-pos)

    # Projection of a point in the reference space

    def projection(self,node,pos):

        residual = np.inf
        parm = np.zeros(2)
        J = np.zeros((2,3))

        # Newton iterations for parametric coordinates

        while np.any(abs(residual)>1e-12):

            x,y = parm
            F = 4*(self.getPosition(node,parm)-pos)
            J[0] = node[0]*(y-1)+node[1]*(1-y)+node[2]*(1+y)-node[3]*(1+y)
            J[1] = node[0]*(x-1)-node[1]*(1+x)+node[2]*(1+x)+node[3]*(1-x)
            residual = np.linalg.lstsq(np.transpose(J),F,-1)[0]
            parm = parm-residual

        return parm
