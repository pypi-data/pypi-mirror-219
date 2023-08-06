from typing import List, Tuple, Union

import numpy as np
import numpy.linalg as LA

# import dask 

xrlbool_ = False
try:
    import xraylib as xrl

    #import xraylib_np as xrlnp
    xrlbool_ = True
    #xrlnp.XRayInit()
    xrl.XRayInit()
except ImportError:
    print("Xraylib not available, using (less benchmarked) own implementation instead")
from . import Constants
from . import material_data as md
from .utils import *


class crystal:
    """A helper class providing basic crystallographic class information about a crystal, including material, orientation, ...
    """
    def __init__(self, Material:str = "Diamond"):
        """Initialize the crystal in default (type dependent) orientation, at 90° angle (pitch-yaw-row format) and room temperature (293 K)

        Args:
            Material (str, optional): [The material type]. Defaults to "Diamond".
        """
        if Material=="Silicon" or Material=="silicon":
            Material=="Si"
        elif Material=="C" or Material=="diamond":
            Material = "Diamond"
        self.material = Material
        self.Tbase = 293
        self.dimensions = 2 #the computational dimensionality
        self.thickness = 1E-3
        self.pitch = np.pi/2.0
        self.roll = 0.0
        self.yaw = 0.0
        self.delta_pitch = 0.0
        self.delta_roll = 0.0
        self.delta_yaw = 0.0
        self.pitch_axes = np.array([1.,0.,0])
        self.roll_axes = np.array([0.,1.,0])
        self.yaw_axes = np.array([0.,0.,1.])
        self.Z = np.linspace(0.,self.thickness,num=60)
        self.disp_Z = np.zeros(self.Z.size,dtype=float)
        self.isstrained = False
        self.R_cryst2lab = np.eye(3)
        self.set_crystal_planes()
        self.calc_RLab2Cryst()
        self.is_strained = False
        if(xrlbool_):
            self.cryst = xrl.Crystal_GetCrystal(Material)
        
    def calc_RLab2Cryst(self):
        """Calculate the rotation matrix to transform 
        from the lab to the crystal frame and vice versa.
        """
        if(self.yaw+self.delta_yaw==0):
            self.R_cryst2lab = np.eye(3)
        else:
            self.R_cryst2lab = Rot_gen(self.yaw+self.delta_yaw, self.yaw_axes)
        if(self.roll+self.delta_roll!=0):
            self.R_cryst2lab = Rot_gen(self.roll+self.delta_roll, self.roll_axes)@self.R_cryst2lab
        if(self.pitch + self.delta_pitch - np.pi/2. != 0):
            self.R_cryst2lab = Rot_gen(np.pi/2. - (self.pitch + self.delta_pitch), self.pitch_axes)@self.R_cryst2lab

        self.R_lab2cryst=self.R_cryst2lab.transpose()
        self.R_H2Lab = self.R_cryst2lab@self.R_H2cryst
        self.R_Lab2H = self.R_H2Lab.transpose()

    def set_crystal_planes(self, i: str="100"):
        """sets the 3D crystallographic orientation of the crystal from a list of predefined orientations. 
        The current list of predefined orientations is:
        "100": z=[-1,0,0]; x=[0,-1/sqrt(2),1/sqrt(2)], y=[0,1/sqrt(2),-1/sqrt(2)]
        "111": z=[-1,-1,-1]/sqrt(3); x=[-1/sqrt(2),1/sqrt(2),0], y=[1/sqrt(6),1/sqrt(6),-2/sqrt(6)]

        Args:
            i (str, optional): the predefined configuration. Defaults to "100".
        """
        if(i=="100"):
            self.R_H2cryst = np.array([
                [0, 1/np.sqrt(2), 1/np.sqrt(2)],
                [0, 1/np.sqrt(2), -1/np.sqrt(2)],
                [-1,0,0]
        ])
        elif(i=="111"):
            self.R_H2cryst = np.array([
                [-1/np.sqrt(2), 1/np.sqrt(2),0],
                [1/np.sqrt(6), 1/np.sqrt(6), -2/np.sqrt(6)],
                [-1/np.sqrt(3),-1/np.sqrt(3),-1/np.sqrt(3)]
            ])
        self.R_cryst2H = self.R_H2cryst.transpose()
        self.R_H2Lab = self.R_cryst2lab@self.R_H2cryst
        self.R_Lab2H = self.R_H2Lab.transpose()

    def set_crystal_planes_xz(self,
        Hx: np.ndarray, Hz: np.ndarray):
        """manually sets the 3D crystallographic orientation of the crystal via definition of the (perpendicular!) x- and z-axis. The y-axis orientation is deduced via the right-hand rule from the other two.

        Args:
            Hx (np.ndarray(shape=3)): the 3D x-axis orientation
            Hz (np.ndarray(shape=3)): [the 3D z-axis orientation]

        Raise:
            AssertionError: orientation vectors must be 3x1 numpy arrays or lists
            AssertionError: orientation vectors must be perpendicular!
        """
        if(type(Hx)==list):
            Hx = np.array(Hx)
        if(type(Hz)==list):
            Hz = np.array(Hz)
        assert type(Hx)==np.ndarray and type(Hz)==np.ndarray, "orientation vectors must be  3x1 numpy arrays"
        assert Hx.size+Hz.size==6, "orientation vectors must be 3d vectors"
        assert np.dot(Hx,Hz)==0, "entered Hx and Hz not perpendicular!" 

        Hx_local = Hx/LA.norm(Hx)
        Hz_local = Hz/LA.norm(Hz)
        Hy_local = np.cross(Hz_local, Hx_local)
        Hy_local = Hy_local/LA.norm(Hy_local)

        self.R_H2cryst = np.array([
                [Hx_local[0], Hx_local[1], Hx_local[2]],
                [Hy_local[0], Hy_local[1], Hy_local[2]],
                [Hz_local[0], Hz_local[1], Hz_local[2]]
        ])

        self.R_cryst2H = self.R_H2cryst.transpose()
        self.R_H2Lab = self.R_cryst2lab@self.R_H2cryst
        self.R_Lab2H = self.R_H2Lab.transpose()

    def set_crystal_planes_xy(self,
        Hx: np.ndarray, Hy: np.ndarray):
        """manually sets the 3D crystallographic orientation of the crystal via definition of the (perpendicular!) x- and y-axis. The z-axis orientation is deduced via the right-hand rule from the other two.

        Args:
            Hx (np.ndarray(shape=3)): the 3D x-axis orientation
            Hy (np.ndarray(shape=3)): [the 3D y-axis orientation]

        Raise:
            AssertionError: orientation vectors must be 3x1 numpy arrays or lists
            AssertionError: orientation vectors must be perpendicular!
        """
        if(type(Hx)==list):
            Hx = np.array(Hx)
        if(type(Hy)==list):
            Hy = np.array(Hy)
        assert type(Hx)==np.ndarray and type(Hy)==np.ndarray, "orientation vectors must be  3x1 numpy arrays"
        assert Hx.size+Hy.size==6, "orientation vectors must be 3d vectors"
        assert np.dot(Hx,Hy)==0, "entered Hx and Hz not perpendicular!" 

        Hx_local = Hx/LA.norm(Hx)
        Hy_local = Hy/LA.norm(Hy)
        Hz_local = np.cross(Hx_local, Hy_local)
        Hz_local = Hz_local/LA.norm(Hz_local)

        self.R_H2cryst = np.array([
                [Hx_local[0], Hx_local[1], Hx_local[2]],
                [Hy_local[0], Hy_local[1], Hy_local[2]],
                [Hz_local[0], Hz_local[1], Hz_local[2]]
        ])

        self.R_cryst2H = self.R_H2cryst.transpose()
        self.R_H2Lab = self.R_cryst2lab@self.R_H2cryst
        self.R_Lab2H = self.R_H2Lab.transpose()

    def set_crystal_planes_z(self, Hz: np.ndarray):
        """manually sets the 3D crystallographic orientation of the crystal via definition of only the z-axis. The x-axis and y-axis orientation are chosen semi-randomly via the right-hand rule from the other z-axis orientation.

        Args:
            Hz (np.ndarray(shape=3)): the 3D z-axis orientation

        Raise:
            AssertionError: orientation vectors must be 3x1 numpy arrays or lists
            AssertionError: orientation vectors must be perpendicular!
        """

        if(type(Hz)==list):
            Hz = np.array(Hz)
        assert type(Hz)==np.ndarray, "orientation vectors must be  3x1 numpy arrays"
        assert Hz.size==3, "orientation vectors must be 3d vectors"

        Hz_local = Hz/LA.norm(Hz)
        dummyVec = np.array([0,0,1])

        if (dummyVec.dot(Hz_local)==1):
            dummyVec = np.array([1,1,1])

        Hx_local = np.cross(dummyVec, Hz_local)
        Hx_local = Hx_local/np.sqrt(np.sum(Hx_local**2))
        Hy_local = np.cross(Hz_local, Hx_local)
        Hy_local = Hy_local/np.sqrt(np.sum(Hy_local**2))

        self.R_H2cryst = np.array([
                [Hx_local[0], Hx_local[1], Hx_local[2]],
                [Hy_local[0], Hy_local[1], Hy_local[2]],
                [Hz_local[0], Hz_local[1], Hz_local[2]]
        ])

        self.R_cryst2H = self.R_H2cryst.transpose()
        self.R_H2Lab = self.R_cryst2lab@self.R_H2cryst
        self.R_Lab2H = self.R_H2Lab.transpose()

    def set_crystal_planes_yz(self,
        Hy: np.ndarray, Hz: np.ndarray):
        """manually sets the 3D crystallographic orientation of the crystal via definition of the (perpendicular!) y- and z-axis. The x-axis orientation is deduced via the right-hand rule from the other two.

        Args:
            Hy (np.ndarray(shape=3)): the 3D y-axis orientation
            Hz (np.ndarray(shape=3)): [the 3D z-axis orientation]

        Raise:
            AssertionError: orientation vectors must be 3x1 numpy arrays or lists
            AssertionError: orientation vectors must be perpendicular!
        """
        if(type(Hy)==list):
            Hy = np.array(Hy)
        if(type(Hz)==list):
            Hz = np.array(Hz)
        assert type(Hz)==np.ndarray and type(Hy)==np.ndarray, "orientation vectors must be  3x1 numpy arrays"
        assert Hz.size+Hy.size==6, "orientation vectors must be 3d vectors"
        assert np.dot(Hz,Hy)==0, "entered Hx and Hz not perpendicular!" 

        Hz_local = Hz/LA.norm(Hz)
        Hy_local = Hy/LA.norm(Hy)
        Hx_local = np.cross(Hy_local, Hz_local)
        Hx_local = Hx_local/LA.norm(Hx_local)

        self.R_H2cryst = np.array([
                [Hx_local[0], Hx_local[1], Hx_local[2]],
                [Hy_local[0], Hy_local[1], Hy_local[2]],
                [Hz_local[0], Hz_local[1], Hz_local[2]]
        ])

        self.R_cryst2H = self.R_H2cryst.transpose()
        self.R_H2Lab = self.R_cryst2lab@self.R_H2cryst
        self.R_Lab2H = self.R_H2Lab.transpose()




    def get_lattice_spacing(self,T: Union[float,int,np.ndarray]) ->np.ndarray :
        """get the crystals' lattice spacing for a specific temperature

        Args:
            T (float, int or np.ndarray[]): int | float) the crystal temperature

        Returns:
            np.ndarray[float]: the lattice spacing
        """
        return md.lattice_spacing(self.material, T)

    def getDBW(self, H: Union[List[float],np.ndarray], T: Union[float,int,list,np.ndarray]) -> np.ndarray:
        """get the debye-waller factor for a given plane H and temperature T

        Args:
            H (array of floats): 3D plane normal
            T (float,int,or np.ndarray]): the crystal temperature(s)

        Returns:
            np.ndarray: the debye-waller factor(s)
        Raise:
            AssertionError: plane vector must be 3x1 numpy array or list
        """
        if(type(H)==list):
            H = np.array(H)
        assert type(H)==np.ndarray, "orientation vectors must be  3x1 numpy arrays"
        assert H.size==3, "orientation vectors must be 3d vectors"
        dbw = md.debye_waller(self.material, T)
        a = self.get_lattice_spacing(T)
        dH = a/np.sqrt(np.sum(H**2)) #only valid for cubic crystal!
        s = 0.5/dH
        return np.exp(-dbw*s*s)

    def getChi(self, E: Union[float, List[float], np.ndarray], H: Union[List[float],np.ndarray], T: Union[float,int,list,np.ndarray]):
        """get the susceptibility for a set of specific energies in eV, temperature in Kelvin and crystal plane. 
        Results differ if xraylib is implemented or not

        Basically just calls getChi_singleE for every E
        Args:
            E (float or list/array of floats): photon energy/ies in eV, 
            H (Union[List[float],np.ndarray]): the crystal plane as 3D vector
            T (Union[float,int,list,np.ndarray]): the crystal temperature(s)
        Returns:
            np.ndarray: 2D array of the complex 0th and Hth order Fourier components of the susceptibilities stored in the columns (second index) 
        """
        E = make_nparray(E)

        return np.array([self.getChi_singleE(Ei, H, T ) for Ei in E])


    def getChi_singleE(self, E: float, H: Union[List[float],np.ndarray], T: Union[float,int,list,np.ndarray]):
        """get the susceptibility for a single specific energy in eV, temperature in Kelvin and crystal plane. 
        Results differ if xraylib is implemented or not

        Args:
            E (float): photon energy in eV, 
            H (Union[List[float],np.ndarray]): the crystal plane as 3D vector
            T (Union[float,int,list,np.ndarray]): the crystal temperature(s)
        Returns:
            List[complex]: tuple of the complex 0th and Hth order Fourier components of the susceptibilities
        """
        E = E*1E-3 
        #Hack:, for some reason xraylib returns Nan if E is smaller than the nominal Theta_Bragg=90° energy of the xrl code
        EB = 0.5*1E+10*1E-3*Constants.h_planck_eV*Constants.c0*np.linalg.norm(H)/self.cryst["a"]
        E_H = E if E>(1+1E-6)*EB else 1.00001*EB 
        a = self.get_lattice_spacing(T)[0]
        #dH = a/np.sqrt(np.sum(H**2))
        #s = 0.5/dH
        F_T = self.getDBW(H, T)

        pre = -Constants.r0_atoms*((Constants.h_planck_eV*Constants.c0/E)**2)/(np.pi*a**3)*1E-6
        if(xrlbool_):
            F_0 = xrl.Crystal_F_H_StructureFactor(self.cryst, E, 0, 0, 0, 1., 1.)
            F_H = xrl.Crystal_F_H_StructureFactor(self.cryst, E_H, int(H[0]), int(H[1]), int(H[2]), F_T[0], 1.)
        else:
            pass
            #TODO: Just a placeholder at the moment! See matlab scripts
        return [pre*(F_0.real -1j*F_0.imag), pre*(F_H.real -1j*F_H.imag)]

    def getChis(self, E: Union[float, List[float], np.ndarray], H: Union[List[float],np.ndarray], T: Union[float,int,list,np.ndarray]):
        """get the susceptibilities for a whole set of planes at a set of specific energies in eV, temperature in Kelvin.
        Results differ if xraylib is implemented or not.

        Just calls the subroutine getChis_singleE for each energy point
        Args:
            E (float or list/array of floats): photon energy/ies in eV,
            H (np.ndarray of dimension n_planes x 3 ]): the crystal planes as list of 3D vectors
            T (Union[float,int,list,np.ndarray]): the crystal temperature(s)
        Returns:
            np.ndarray: E-points x n_planes+1 x nplanes+1 dimensional array of the complex susceptibilities, with the diagonal corresponding to the 0th order Fourier component
        """
        E = make_nparray(E)

        return np.array([self.getChis_singleE(Ei, H, T ) for Ei in E])


    def getChis_singleE(self, E: float, H: Union[List[float],np.ndarray], T: Union[float,int,list,np.ndarray]):
        """get the susceptibilities for a whole set of planes at a single specific energy in eV, temperature in Kelvin.
        Results differ if xraylib is implemented or not
        Args:
            E (float): photon energy in eV, 
            H (np.ndarray of dimension n_planes x 3 ]): the crystal planes as list of 3D vectors
            T (Union[float,int,list,np.ndarray]): the crystal temperature(s)
        Returns:
            np.ndarray: n_planes+1 x nplanes+1 dimensional array of the complex susceptibilities, with the diagonal corresponding to the 0th order Fourier component
        """
        E = E*1E-3
        #FIXME: Dirty hack, for some reason xraylib returns Nan if E is smaller than the nominal Theta_Bragg=90° energy of the xrl code
        EB = 0.5*1E+10*1E-3*Constants.h_planck_eV*Constants.c0*np.linalg.norm(H)/self.cryst["a"]
        E_H = E if E>(1+1E-6)*EB else 1.00001*EB 


        nplanes = H.shape[0]

        xArray = np.ndarray([nplanes+1,nplanes+1],dtype=complex)
        
        a = self.get_lattice_spacing(T)[0]
        dbw = md.debye_waller(self.material,T)
        pre = -Constants.r0_atoms*((Constants.h_planck_eV*Constants.c0/E)**2)/(np.pi*a**3)*1E-6
      
        if(xrlbool_):
            F0 = xrl.Crystal_F_H_StructureFactor(self.cryst, E, 0, 0, 0, 1., 1.)
        else:
            F0 = 0 + 0j #TODO: Placeholder
        x0h = pre*(F0.real-1j*F0.imag)

        Hplane_dummy = np.vstack([np.zeros([1,3],dtype=int),H])
        Hd = np.ndarray(3,dtype=int)
        for I1 in range(nplanes+1):
            for I2 in range(nplanes+1):
                if( I1 == I2):
                    xArray[I1,I2]=x0h 
                else:
                    Hd = Hplane_dummy[I1,:] - Hplane_dummy[I2,:]
                    dH=a/np.sqrt(np.sum(Hd**2))
                    s = 0.5/dH
                    F_T = np.exp(-dbw*s*s)
                    if(xrlbool_):
                        F_H = xrl.Crystal_F_H_StructureFactor(self.cryst, E_H,int(Hd[0]), int(Hd[1]), int(Hd[2]), F_T[0], 1.)
                    else:
                        FH = 0 + 0j #TODO: Placeholder
                    xArray[I1,I2] = pre*(F_H.real - 1j*F_H.imag)
        return xArray

    def z_Surf(self) -> np.ndarray:
        """Returns the surface plane

        Returns:
            np.ndarray: the surface plane
        """
        return self.R_cryst2H[:,2]
    def x(self) -> np.ndarray:
        """Returns the x-directed plane

        Returns:
            np.ndarray: the x-orientation
        """
        return self.R_cryst2H[:,0]

    def y(self) -> np.ndarray:
        """Returns the y-directed plane

        Returns:
            np.ndarray: the y-orientation
        """
        return self.R_cryst2H[:,1]
#cr = crystal()

#print(cr.cryst['name'])

