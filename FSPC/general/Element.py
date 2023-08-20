import numpy as np

# %% Linear Line Finite Element

class Line(object):

    def evaluate(self,parm):
        return np.array([(1-parm[0])/2,(1+parm[0])/2])

    # Interpolate nodal data in the parametric space

    def interpolate(self,nodeVal,parm):
        return np.squeeze(self.evaluate(parm).dot(nodeVal))
    
    # Projection of a point in the parametric space

    def projection(self,node,pos):
    
        A = np.diff(node,axis=0)/2
        B = np.array(pos-np.sum(node,axis=0)/2)
        return np.linalg.lstsq(np.transpose(A),B,-1)[0]

    # Distance between a point and the projection

    def distance(self,parm,node,pos):

        if abs(parm)>1.001: return np.inf
        return np.linalg.norm(self.interpolate(node,parm)-pos)

# %% Linear Triangle Finite Element

class Triangle(Line):

    def evaluate(self,parm):
        return np.array([1-parm[0]-parm[1],parm[0],parm[1]])
    
    # Projection of a point in the parametric space

    def projection(self,node,pos):

        B = np.array(pos-node[0])
        A = [node[1]-node[0],node[2]-node[0]]
        return np.linalg.lstsq(np.transpose(A),B,-1)[0]

    # Distance between a point and the projection

    def distance(self,parm,node,pos):

        if any(-0.001>parm) or sum(parm)>1.001: return np.inf
        return np.linalg.norm(self.interpolate(node,parm)-pos)

# %% Linear Quadrangle Finite Element

class Quadrangle(Line):

    def evaluate(self,parm):

        return np.array([
        (1-parm[0])*(1-parm[1])/4,(1+parm[0])*(1-parm[1])/4,
        (1+parm[0])*(1+parm[1])/4,(1-parm[0])*(1+parm[1])/4])
    
    # Gradient of the element shape functions
    
    def grad(self,parm):

        return np.array([
        [(parm[1]-1)/4,(1-parm[1])/4,(1+parm[1])/4,(-parm[1]-1)/4],
        [(parm[0]-1)/4,(-parm[0]-1)/4,(1+parm[0])/4,(1-parm[0])/4]])
    
    # Distance between a point and the projection

    def distance(self,parm,node,pos):

        if any(abs(parm)>1.001): return np.inf
        return np.linalg.norm(self.interpolate(node,parm)-pos)

    # Projection of a point in the parametric space

    def projection(self,node,pos):

        residual = np.inf
        parm = np.zeros(2)
        
        # Newton iterations for parametric coordinates

        for i in range(25):

            A = self.grad(parm).dot(node)
            B = self.interpolate(node,parm)-pos
            residual = np.linalg.lstsq(np.transpose(A),B,-1)[0]
            parm = parm-residual

            if np.all(abs(residual) < 1e-12): return parm
        return np.array([np.inf,np.inf])
    