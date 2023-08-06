#route directory to core
import sys
sys.path.append("..")

#import core as we would CalSim
import core as cs
import numpy as np
import matplotlib.pyplot as plt

#system initial condition
x0 = np.array([[0, 0, 0]]).T

#create a dynamics object for the double integrator
dynamics = cs.TurtlebotSysDyn(x0, N = 1)

#create an obstacle
qObs = np.array([[0, 1, 1], [0, 0.5, 2]]).T
rObs = [0.25, 0.25]
obstacleManager = cs.ObstacleManager(qObs, rObs, NumObs = 2)

#create an observer
observerManager = cs.ObserverManager(dynamics)

#create a depth camera
depthManager = cs.DepthCamManager(observerManager, obstacleManager, mean = None, sd = None)

# create a controller manager with a basic FF controller
controllerManager = cs.ControllerManager(observerManager, cs.FFController)

env = cs.Environment(dynamics, controllerManager, observerManager)
env.reset()

#test the pointcoud
ptcloudDict = depthManager.get_depth_cam_i(0).get_pointcloud()
ptcloudTurtle = ptcloudDict["ptcloud"]
x = ptcloudTurtle[0, :].tolist()
y = ptcloudTurtle[1, :].tolist()

#plot the pointcloud
plt.plot(x, y)
plt.show()

# #run the simulation
# env.run()