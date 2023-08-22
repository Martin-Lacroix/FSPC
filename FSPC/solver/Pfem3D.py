from ..general import Toolbox as tb
import pfem3Dw as w
import numpy as np
import gmsh

# %% Initializes the Fluid Wraper

class Pfem3D(object):
    def __init__(self,path):

        # Incompressible or weakly compressible solver

        self.problem = w.getProblem(path)
        if 'WC' in self.problem.getID():
            
            self.implicit = False
            self.run = self.runExplicit
            self.maxDivision = 200

        else:
            
            self.implicit = True
            self.run = self.runImplicit
            self.maxDivision = 10

        # Store the important objects and variables

        self.FSI = w.VectorInt()
        self.mesh = self.problem.getMesh()
        self.solver = self.problem.getSolver()
        self.dim = self.mesh.getDim()
        self.initialize()

        # Save mesh after initializing the BC pointer

        self.prevSolution = w.SolutionData()
        self.problem.copySolution(self.prevSolution)
        self.problem.displayParams()

# %% Run for implicit integration scheme

    @tb.write_logs
    @tb.compute_time
    def runImplicit(self):

        dt = tb.step.dt
        t2 = tb.step.nexTime()
        print('\nt = {:.5e} - dt = {:.5e}'.format(t2,dt))

        self.problem.loadSolution(self.prevSolution)
        count = int(1)

        # Main solving loop for the fluid simulation

        while count > 0:
            
            self.solver.setTimeStep(dt)
            if not self.solver.solveOneTimeStep():
                
                dt = float(dt/2)
                count = np.multiply(2,count)
                if dt < tb.step.dt/self.maxDivision: return False
                continue

            count = count-1
        return True

# %% Run for explicit integration scheme

    @tb.write_logs
    @tb.compute_time
    def runExplicit(self):

        dt = tb.step.dt
        t2 = tb.step.nexTime()
        print('\nt = {:.5e} - dt = {:.5e}'.format(t2,dt))

        self.problem.loadSolution(self.prevSolution)
        iteration = 0

        # Estimate the time step for stability

        self.solver.computeNextDT()
        division = int(dt/self.solver.getTimeStep())
        if division > self.maxDivision: return False
        dt = dt/division

        # Main solving loop for the fluid simulation

        while iteration < division:
    
            iteration += 1
            self.solver.setTimeStep(dt)
            self.solver.solveOneTimeStep()

        return True

# %% Dirichlet Boundary Conditions

    def applyPosition(self,pos):

        BC = (pos-self.pos)/tb.step.dt
        if not self.implicit: BC = 2*(BC-self.vel)/tb.step.dt

        for i,vector in enumerate(BC):
            for j,val in enumerate(vector): self.BC[i][j] = val

    # Update the Dirichlet nodal temperature

    def applyTemperature(self,temp):

        for i,vector in enumerate(temp):
            self.BC[i][self.dim] = vector[0]
            
# %% Return Nodal Values

    def getPosition(self):

        vector = np.zeros((self.nbrNod,self.dim))

        for i in range(self.dim):
            for j,k in enumerate(self.FSI):
                vector[j,i] = self.mesh.getNode(k).getCoordinate(i)

        return vector

    # Computes the nodal velocity vector

    def getVelocity(self):

        vector = np.zeros((self.nbrNod,self.dim))
        
        for i in range(self.dim):
            for j,k in enumerate(self.FSI):
                vector[j,i] = self.mesh.getNode(k).getState(i)

        return vector
        
    # Mechanical boundary conditions

    @tb.compute_time
    def getLoading(self):

        vector = w.VectorVectorDouble()
        self.solver.computeStress('FSInterface',self.FSI,vector)
        return np.copy(vector)

    # Thermal boundary conditions

    @tb.compute_time
    def getHeatFlux(self):

        vector = w.VectorVectorDouble()
        self.solver.computeHeatFlux('FSInterface',self.FSI,vector)
        return np.copy(vector)

# %% Initialize Communication Vectors

    def initialize(self):

        self.mesh.getNodesIndex('FSInterface',self.FSI)
        self.nbrNod = self.FSI.size()
        self.BC = list()

        for i in self.FSI:

            vector = w.VectorDouble(self.dim+1)
            self.mesh.getNode(i).setExtState(vector)
            self.BC.append(vector)

        # Store temporary simulation variables

        self.pos = self.getPosition()
        self.vel = self.getVelocity()

# %% Other Functions

    @tb.compute_time
    def update(self):

        self.mesh.remesh(False)
        if self.implicit: self.solver.precomputeMatrix()
        self.problem.copySolution(self.prevSolution)
        self.pos = self.getPosition()
        self.vel = self.getVelocity()

    # Save the results or finalize

    @tb.write_logs
    @tb.compute_time
    def save(self): self.problem.dump()

    @tb.write_logs
    def exit(self): self.problem.displayTimeStats()

# %% FSI Facets Relative to Each Node

    @tb.compute_time
    def getFacet(self):

        if not gmsh.isInitialized(): gmsh.initialize()
        gmsh.option.setNumber('General.Terminal',0)
        file = self.mesh.getInfos().mshFile
        gmsh.open(file)

        # Find the tag of FSInterface physical group

        for data in gmsh.model.getPhysicalGroups():
            group = gmsh.model.getPhysicalName(*data)
            if 'FSInterface' == group: physical = data

        faceList = list()
        entity = gmsh.model.getEntitiesForPhysicalGroup(*physical)

        # Node with coordinates and elements of the interface

        for tag in entity:
            faceList.append(gmsh.model.mesh.getElements(physical[0],tag)[2])

        faceList = np.ravel(np.concatenate(faceList,axis=1))
        nodeTags,coord = gmsh.model.mesh.getNodesForPhysicalGroup(*physical)
        coord = np.reshape(coord,(len(nodeTags),3))[:,:self.dim]
        gmsh.finalize()

        # Make the tag to index vector converter

        index = np.zeros(int(max(nodeTags))+1,dtype=int)-1
        for i,tag in enumerate(nodeTags): index[tag] = i
        vectorPos = self.getPosition()

        for i,tag in enumerate(faceList):

            position = coord[index[tag]]
            distance = np.linalg.norm(position-vectorPos,axis=1)
            idx = np.argmin(distance)
            faceList[i] = idx

        faceList = np.reshape(faceList,(-1,self.dim))
        return faceList