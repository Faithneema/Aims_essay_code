# DATA COMPONENTS
from yade import utils
from yade import qt
from yade import *
from yade import pack, plot, geom
from math import *
#from fenics import *
import sys

#from pylab import *
#######################################################3
utils.readParamsFromTable(n=1,dens=2500,frict=35.3,E=4e5,coh=1e4,eta=5)
from yade.params.table import *
##########################################################
#granular material data
particlematerial=CohFrictMat(young=E,poisson=.2,density=dens,
frictionAngle=radians(frict),normalCohesion=coh,
shearCohesion=coh,momentRotationLaw=True,etaRoll=eta,etaTwist=eta)
O.materials.append(particlematerial)
##################################################################
#sp=pack.SpherePack()
# generate randomly spheres with uniform radius distribution
#sp.makeCloud((0,0,0),(1,1,1),rMean=.3,rRelFuzz=.5)
# add the sphere pack to the simulation
#sp.toSimulation()
#################  Particles   ##############################
#O.bodies.append([utils.sphere((0,0,3),.5),utils.sphere(center=(0,0,5),radius=.5)])
#######
r1=0.034  ## in mm
sp=pack.SpherePack()
# generate randomly spheres with uniform radius distribution
sp.makeCloud((.4,0,-1.0),(1.4,1.0,1.0),rMean=r1,rRelFuzz=0.35,num=4000)
#sp.makeCloud((.2,0,-0.5),(0.7,0.5,0.5),rMean=r1,rRelFuzz=0)
#sp.makeCloud((-.1,-.1,.1),(.1,.1,.6),rMean=.02,rRelFuzz=0)#
#sp.toSimulation()
#O.bodies.append(utils.wall(-1,axis=2))
sp.toSimulation(color=(1,1,1)) # pure green
#ids = sp1.toSimulation(color=(1,0,0)) # add the result to simulation with uniform color
###################################################
sampling=.01 #second
omega=2*pi*0.31
###################### cylinder  ################################1
cylinder=O.bodies.append(geom.facetCylinder(center=(1,0,0),
radius=1.2,height=1,orientation=utils.Quaternion((1,0,0),pi/2),
segmentsNumber=33,wallMask=7,color=(1,1,1),angleRange=None, wire=True))
#.bodies.append(utils.wall((0,,-10),axis=2))
############################ Helix #####################################
#O.bodies.append(utils.geom.facetHelix(center=(1,1,0), radiusOuter=0.6, pitch=1, orientation=utils.Quaternion((1, 0, 0), pi/2), 
#segmentsNumber=25, angleRange=None, radiusInner=0.1, wire=False, color=(0,1,0) ))
######################## Engines ###############################
from yade import *
O.engines=[
         ForceResetter(),
         InsertionSortCollider([Bo1_Sphere_Aabb(),Bo1_Facet_Aabb()]),
         InteractionLoop(
           [Ig2_Sphere_Sphere_ScGeom6D(),Ig2_Facet_Sphere_ScGeom()],
           [Ip2_FrictMat_FrictMat_FrictPhys(),
            Ip2_CohFrictMat_CohFrictMat_CohFrictPhys(label="cohesiveIp")],
          [Law2_ScGeom_FrictPhys_CundallStrack(),
          Law2_ScGeom6D_CohFrictPhys_CohesionMoment(useIncrementalForm=True,
          always_use_moment_law=True,label='cohesiveLaw')]
),
     NewtonIntegrator(gravity=(0,0,-9.8),damping=.1),
     RotationEngine(rotateAroundZero=True,zeroPoint=(1,0,0),
          rotationAxis=(0,1,0),angularVelocity=omega, ids = cylinder),
PyRunner(command='checkUnbalanced()',realPeriod=5),
PyRunner(command='addPlotData()',realPeriod=5)
]
###########################################################################
O.dt=0.5*utils.PWaveTimeStep()
O.trackEnergy=True
#O.step()
#######################################################







def checkUnbalanced():
	if unbalancedForce()<.05:
		#O.pause()
		plot.saveDataTxt('bbb.txt.bz2')
###################################################################
#def addPlotData():
	#plot.addData(Time=O.time,**O.energy)


#def addPlotData():
	#b=O.bodies[1]
	#plot.addData(Positionz1=b.state.pos[2], Velocity1=b.state.vel.norm(), i=O.iter, Time=O.time)
def addPlotData():
# this function adds current values to the history of data, under the names specified
	plot.addData(Time=O.time,Torque1=utils.sumTorques,CoordinationNumber=utils.avgNumInteractions(),Unbalancedforce=utils.unbalancedForce(),**O.energy)
#plot.plots={  'Time':('Positionz1')}
#plot.plots={  'Time':['twistDissip','bendingDissip']}
plot.plots={ 'Time':['gravWork','kinetic']}
#plot.plots={   'Time':['nonviscDamp']}
#plot.plots={   'Time ':('plastDissip','twistDissip')}
#plot.plots={'Time':('coordNum','unForce',None,'Ek') }
#plot.plots={ 'Time':['unForce'] , 'Time ':('coordNum')}

#plot.plots={   'Time ':('CoordinationNumber')}
#plot.plots={   'Time ':('Unbalancedforce')}
#plot.plots={'i':('unbalanced',None,O.energy.keys)}
# show the plot on the screen, and update while the simulation runs
#plot.plot()
plot.plot(subPlots=False)
O.saveTmp()
#####################################
# this function is called when the simulation is finished
#def finish():
   # snapshot is label of qt.SnapshotEngine
   # the 'snapshots' attribute contains list of all saved files
   #makeVideo(snapshot.snapshots,'3d.mpeg',fps=10,bps=10000)
   #O.pause()


v=qt.View()
#O.run()

