import numpy as np
from .state_estimation import *

"""
File containing controllers 
"""
class Controller:
    def __init__(self, observer, lyapunovBarrierList = None, trajectory = None, depthCam = None):
        """
        Skeleton class for feedback controllers
        Args:
            observer (Observer): state observer object
            lyapunov (List of LyapunovBarrier): list of LyapunovBarrier objects
            trajectory (Trajectory): trajectory for the controller to track (could just be a constant point!)
            depthCam (PlanarDepthCam or Lidar): depth camera object
        """
        #store input parameters
        self.observer = observer
        self.lyapunovBarrierList = lyapunovBarrierList
        self.trajectory = trajectory
        self.depthCam = depthCam
        
        #store input
        self._u = np.zeros((self.observer.singleInputDimn, 1))
    
    def eval_input(self, t):
        """
        Solve for and return control input
        Inputs:
            t (float): time in simulation
        Returns:
            u ((Dynamics.singleInputDimn x 1)): input vector, as determined by controller
        """
        self._u = np.zeros((self.observer.singleInputDimn, 1))
        return self._u
    
    def get_input(self):
        """
        Retrieves input stored in class parameter
        Returns:
            self._u: most recent input stored in class paramter
        """
        return self._u
    
class FFController(Controller):
    """
    Class for a simple feedforward controller.
    """
    def __init__(self, observer, lyapunovBarrierList = None, trajectory = None, depthCam = None):
        """
        Init function for a ff controller
        Args:
            observer (Observer): state observer object
            ff (NumPy Array): constant feedforward input to send to system
            lyapunov (List of LyapunovBarrier): list of LyapunovBarrier objects
            trajectory (Trajectory): trajectory for the controller to track (could just be a constant point!)
        """
        self.ff = np.array([[9.81*0.92, 0]]).T
        self.depthCam = depthCam
        super().__init__(observer, lyapunovBarrierList, trajectory)
    
    def eval_input(self, t):
        """
        Solve for and return control input
        Inputs:
            t (float): time in simulation
        Returns:
            u ((Dynamics.singleInputDimn x 1)): input vector, as determined by controller
        """
        if self.depthCam is not None:
            #test the depth camera
            self.depthCam.get_pointcloud()

        self._u = self.ff
        return self._u