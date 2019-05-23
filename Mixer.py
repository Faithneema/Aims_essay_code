
from yade import utils
from yade import qt
from yade import *
from yade import pack, plot, geom
from math import *
import sys
import pylab 
import random as random


#Add material of particles to simulation
#O.materials.append((FrictMat(young=30e9,poisson=0.2,frictionAngle=0.6),FrictMat(young=30e9,poisson=0.2,frictionAngle=0.6)))

O.materials.append((FrictMat(young=210e9,density=2400,poisson=0.25,frictionAngle=0.8),FrictMat(young=30e9,density=2400,frictionAngle=0.6,poisson=0.2)))

#Defining radius of particles
r2 = 0.2
r1 = 0.2

#create empty  loose pack of spheres
sp1 = pack.SpherePack()
sp2 = pack.SpherePack()

#generate random sphere with exactly same radius radius
#sp1.makeCloud((-3,0,-3),(3,3,3),rMean=r1)
#sp2.makeCloud((-3,3,-3),(3,6,6),rMean=r2)


sp1.makeCloud((-3,0,-6),(0,6,6),rMean=r1,num=10)
sp2.makeCloud((0,0,-6),(3,6,6),rMean=r2,num=10)



#Add spheres to simulation
sp1.toSimulation(color=(0.7,0,0))
sp2.toSimulation(color=(0,0.7,0))


#creating a box from facets#~box=O.bodies.append(geom.facetBox(center=(0,0,0),extents=(6,6,6),orientation=utils.Quaternion((1,0,0),0),wallMask=63))


Helix = O.bodies.append(geom.facetHelix(center = (0,7,0), radiusOuter=6.5, pitch=5, orientation=utils.Quaternion((1, 0, 0), pi/2), segmentsNumber=19, color=(0.3,0.3,0.3), angleRange=(0,5.5*pi), radiusInner=0, wire=False))

#Helix1 = O.bodies.append(geom.facetHelix(center = (0,6,0), radiusOuter=5.5, pitch=2.8, orientation=utils.Quaternion((1,0, 0), pi/2),color=(0.8,0.8,0.8), segmentsNumber=19, angleRange=(0,10*pi), radiusInner=0,wire=False))

#Helix2 = O.bodies.append(geom.facetHelix(center = (0,5,0), radiusOuter=4.5, pitch=2.5, orientation=utils.Quaternion((1,0, 0), pi/2),color=(0,0,1), segmentsNumber=19, angleRange=(0,10*pi), radiusInner=0,wire=False))


#Helix = O.bodies.append(geom.facetHelix(center = (0,0,0), radiusOuter=6, pitch=1, orientation=utils.Quaternion((0, 1, 1), pi/2), segmentsNumber=10, angleRange=None, radiusInner=0))


#Helix = O.bodies.append(geom.facetHelix(center = (0,0,0), radiusOuter=6, pitch=1, orientation=utils.Quaternion((1, 1, 0), pi), segmentsNumber=100, angleRange=None, radiusInner=0))




#Creating a cylinder from facets
Cylinder=O.bodies.append(geom.facetCylinder(center=(0,0,0),radius=7,height=14,orientation=utils.Quaternion((1,0,0),pi/2),    segmentsNumber=15,wallMask=7,color=(0.3,0.3,0.3),angleRange=None,  closeGap=True))



O.engines=[
 ForceResetter(),
InsertionSortCollider([Bo1_Sphere_Aabb(),Bo1_Facet_Aabb(),Bo1_Wall_Aabb()]),
 InteractionLoop(
  [Ig2_Sphere_Sphere_ScGeom6D(),Ig2_Facet_Sphere_ScGeom(),Ig2_Wall_Sphere_ScGeom()],

  [Ip2_FrictMat_FrictMat_FrictPhys()],
  [Law2_ScGeom_FrictPhys_CundallStrack()]),
   NewtonIntegrator(gravity=(0,-9.8,0),damping=.4,label="newtonCustomLabel"),
   HelixEngine(rotateAroundZero=True,linearVelocity=0.0,rotationAxis=(0,1,0),angularVelocity=40, ids = Helix),#HelixEngine(rotateAroundZero=True,linearVelocity=0.0,rotationAxis=(0,1,0),angularVelocity=40, ids = Helix1),HelixEngine(rotateAroundZero=True,linearVelocity=0.0,rotationAxis=(0,1,0),angularVelocity=40, ids = Helix2),

qt.SnapshotEngine(fileBase='3d-', realPeriod=5000, label='snapshot'),
]



O.dt=0.6*utils.PWaveTimeStep()




print O.iter 
v=qt.View();

