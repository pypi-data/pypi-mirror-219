"""Small utility functions

    Functions:
    Check3D(x): checks if the input x is a 3D vector
    make_nparray(x): makes a numpy array from input x
    normalize(x): normalizes a vector x  
"""
import numpy as np


def check3D(x) -> np.ndarray:
    """checks if the input is a 3D vector

    Args:
        x : Input to check
    
    Returns:
        np.ndarray: numpy array of input

    Raises:
        TypeError: if input x is not 3D array (either list or np.ndarray)
    """
    if(type(x)==list):
            x = np.array(x)
    
    if (type(x)!=np.ndarray or x.size!=3): 
        raise TypeError("vector must be 3x1 array")
    return x
    
def make_nparray(x)->np.ndarray:
    """Make numeric numpy array from entry

    Args:
        x ([type]): The input
    Returns:
        np.ndarray: The numpy array of the entry
    Raises:
        TypeError: input must be of numeric type
    """
    if(type(x)!=np.ndarray):
        if(type(x)==list or type(x)==tuple):
            x = np.array(x)
        else:
            x = np.array([x])
    try:
        x/2
    except:
        raise(TypeError("x must be of numeric type"))
    return x



def normalize(x:np.ndarray):
    """normalize input vector x

    Args:
        x (np.ndarray): input vector

    Raises:
        TypeError: input must be np.ndarray

    Returns:
        np.ndarray: normalized vector
    """
    if(type(x)!=np.ndarray): raise TypeError("Input must be numpy array.")
    return x/np.sqrt(np.sum(x**2))

def rad2deg(x:float):
    return x*180./np.pi

def deg2rad(x:float):
    return x*np.pi/180.

def Rot_gen(alpha:float, u:np.ndarray=np.array([1.,0,0])) -> np.ndarray:
    """General 3x3 rotation matrix about alpha [rad] around arbitrary axis u

    Args:
        alpha ([float]): rotation angle in radians
        u ([np.ndarray]): 3D rotation axis. Defaults to x-axis).
    Raise: 
        AssertionError: rotation axis must be 3x1 numpy array or list
    """
    if(type(u)==list):
        u = np.array(u)
    assert type(u) == np.ndarray, "u must be a 3x1 numpy array"
    assert u.size == 3, "u must be a 3 dimensional vector!"
    u = u/np.linalg.norm(u)

    if(u[0] == 1.): #rotation around x-axis
        return np.array([[1,0,0],
        [0, np.cos(alpha), -np.sin(alpha)],
        [0, np.sin(alpha), np.cos(alpha)]])
    elif(u[1] == 1.):#rotation around y-axis
        return np.array([[np.cos(alpha), 0,np.sin(alpha)],
        [0, 1, 0],
        [-np.sin(alpha), 0, np.cos(alpha)]])
    elif(u[2] == 1.):#rotation around z-axis
        return np.array([[np.cos(alpha), -np.sin(alpha), 0], 
        [np.sin(alpha), np.cos(alpha), 0],
        [0, 0, 1]])
    else: #rotation around arbitrary axis
        return np.array([[
            u[0]*u[0]*(1-np.cos(alpha))+np.cos(alpha), u[0]*u[1]*(1-np.cos(alpha)) - u[2]*np.sin(alpha), u[0]*u[2]*(1-np.cos(alpha))+u[1]*np.sin(alpha)], 
        [u[1]*u[0]*(1-np.cos(alpha))+u[2]*np.sin(alpha), u[1]*u[1]*(1-np.cos(alpha)) + np.cos(alpha), u[1]*u[2]*(1-np.cos(alpha))-u[0]*np.sin(alpha)],
        [u[2]*u[0]*(1-np.cos(alpha))-u[1]*np.sin(alpha), u[2]*u[1]*(1-np.cos(alpha)) + u[0]*np.sin(alpha), u[2]*u[2]*(1-np.cos(alpha))+ np.cos(alpha)]
        ])
    
