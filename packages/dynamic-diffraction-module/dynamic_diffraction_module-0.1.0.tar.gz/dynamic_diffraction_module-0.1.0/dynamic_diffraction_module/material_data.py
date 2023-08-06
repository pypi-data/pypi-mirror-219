"""Returns material specific data, currently only for diamond and silicon


Functions:
    lattice_spacing(str, float/int or np.ndarray)->np.ndarray
    debye_waller(str, float/int or np.ndarray)->np.ndarray
"""
import os
from typing import Union

import numpy as np

Path_mat = os.path.dirname(os.path.realpath(__file__)) +"/data_files/"

def lattice_spacing(mat: str, T: Union[float,np.ndarray]) ->np.ndarray:
    """get the lattice spacing of a specific material at temperature T

    Args:
        mat (str): The Material type, currently only "Diamond" and "Silicon" are available
        T (float/int or np.ndarray): the temperature(s) in Kelvin
    Returns:
        np.ndarray: The lattice spacing at temperature(s) T
    Raises:
        TypeError: if temperature is not a number or array/list of numbers
        AssertionError: if the material type is neither diamond or silicon
    """
    if(type(T)==float or type(T)==int):
        T = np.array([T],dtype=float)
    elif(type(T)==list):
        T = np.array(T)
    else:
        raise TypeError("temperature T must be float, int or of corresponding array-type")
    a = np.ndarray(T.shape)
    if(mat=="Diamond" or mat=="diamond" or mat=="C"):
        a298 = 3.56712e-10
        Th_exp = np.array([159.3,548.5,1237.9,2117.8])
        Xi_exp = np.array([0.0096e-6,0.2656e-6,2.6799e-6,2.3303e-6])

        a = np.array([a298*(1+np.sum(
            Xi_exp*Th_exp*(
                1/(np.exp(Th_exp/T_)-1) - 1/(np.exp(Th_exp/298)-1))
            )) for T_ in T])
    elif(mat=="Silicon" or mat=="silicon" or mat=="Si"):

        a295 = 5.431020*1E-10
        T0 = 295
        expand = np.loadtxt(Path_mat + "alpha_si.dat")
        for idx,T_ in enumerate(T):
            if(T_!=T0):
                index = [np.argmin(np.abs(expand[:,0]-T_)),np.argmin(np.abs(expand[:,0]-T0))]
                if(T_<T0):
                    dummy = -np.trapz(expand[index[0]:index[1],1],expand[index[0]:index[1],0])*1E-6
                else:
                    dummy =  np.trapz(expand[index[1]:index[0],1],expand[index[1]:index[0],0])*1E-6
            
                a[idx] = a295*np.exp(dummy)
            else:
                a[idx] = a295
    else:
        raise AssertionError("The material \"" + mat + "\" is not supported yet" )
    return a


def debye_waller(mat: str, T: Union[float,int,np.ndarray]) -> np.ndarray:
    """calculate the material and temperature specific debye-waller factor (DBW) in m²

    Args:
        mat (str): The Material type, currently only "Diamond" and "Silicon" are available
        T (float, int or np.ndarray): the temperature(s) in Kelvin

    Returns:
        np.ndarray: The DBW at temperature(s) T
    Raises:
        TypeError: if temperature is not a number or array/list of numbers
        AssertionError: if the material type is neither diamond or silicon
    Long: 
        The routine computes the Debye-Waller temperature factor by a 4th order polynomial fit done by H. X. Gao aand L.-M. Peng [1] to various experimental data for different materials 
        [1] H.X. Gao and L.-M. Peng, Acta Cryst(1999), A55, 926-932
    """
    if(type(T)==float or type(T)==int):
        T = np.array([T],dtype=float)
    elif(type(T)==list):
        T = np.array(T)
    if(type(T)!=np.ndarray):
        raise TypeError("temperature T must be float, int or of corresponding array-type")
    DBW = np.ndarray(T.shape,dtype=float)
    Tpow = np.array([T**i for i in np.arange(5)])
    adbw = np.ndarray([5,T.size])
    index80 = T<=80
    if (mat=="Diamond" or mat=="diamond" or mat=="C"):
        for idx in range(T.size):
            if(index80[idx]):
                adbw[:,idx] = np.array([0.11918, -0.6360E-07, 0.1962E-06, 0.3167E-09, -0.1858E-11])
            else:
                adbw[:,idx] = np.array([0.12034, -0.2231E-04, 0.3348E-06, -0.2108E-09, 0.5320E-13])
    elif(mat=="Silicon" or mat=="silicon" or mat=="Si"):
        for idx in range(T.size):
            if(index80[idx]):
                adbw[:,idx] = np.array([0.19284, 0.1670E-04, -0.7475E-06, 0.1410E-06, -0.8174E-09])
            else:
                adbw[:,idx] = np.array([0.14236, 0.9261E-03, 0.1623E-05, -0.1677E-08, 0.6351E-12])
    else:
        raise AssertionError("The material \"" + mat + "\" is not supported yet" )
    return 4*(1E-20/3)*np.sum(adbw*Tpow,axis=0).reshape(T.shape)
    
