"""Functionality for doing dynamic diffraction calculations for "Bragg mirrors"

classes:
    bmirror
"""

#from kiwisolver import Constraint

from typing import List, Tuple, Union

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.optimize as opt
from mpl_toolkits import mplot3d
from numpy.core.fromnumeric import prod
from numpy.lib import emath

from . import Constants
from . import material_data as md
from .crystal import crystal
from .utils import *

#from sympy import construct_domain
#import dask


prop_cycle = plt.rcParams['axes.prop_cycle']
colors = prop_cycle.by_key()['color']

class bmirror:
    """This class provides functionality for doing dynamic diffraction related calculation for crystal mirrors.
    The class makes use of the crystal class from the crystal module
    """

    def __init__(self, H0: Union[List[float], List[int], np.ndarray] = np.array([1, 0, 0]), cryst: Union[str, crystal] = "Diamond", twoBFlag_=True):
        """initialize the base parameters of the Bragg mirror for a chosen mirror plane H0.
        Either uses a predefined crystal or defines a default configuration for a specified material

        Args:
            H0 (List or np.ndarray of floats or ints ): the mirror plane of interest
            defaults to [1,0,0]  
            cryst (Union[str, crystal], optional): Either the material type, defining a default crystal configuration, or a predefined crystal. Latter is recommended. Defaults to "Diamond".

        Raises:
            TypeError: If the input is neither string or crystal type.
            TypeError: plane vectors must be 3x1 numpy arrays or lists
        """
        self.H0 = check3D(H0)
        if(type(cryst) == str):
            print(
                "initializing Bragg mirror from string: Default (symmetric) crystal configuration")
            cryst = crystal(cryst)
            cryst.set_crystal_planes_z(-self.H0)
        elif(type(cryst) == crystal):
            print("initializing Bragg mirror from predefined crystal")
        else:
            raise TypeError(
                "The input must either be of string or of crystal type")
        
        if cryst.material == "Diamond":
            self.df_Hplanes = pd.read_csv(md.Path_mat+"Hplanes_C.csv") #all possible Hplanes in a pandas dataframe
            self.df_Hplanes['hkl'] = [np.fromstring(a.replace('[','').replace(']',''),count=3,sep=' ',dtype=int) for a in self.df_Hplanes['hkl']] #'hkl' will be read in as string 

        self.cryst = cryst
        self.twoBFlag = twoBFlag_
        # the polarization of the incoming radiation is per default in x-direction
        self.polInLab = np.array([1, 0, 0])
        self.KInLab = np.array([0, 0, 1])

        self.initialize()

    def getAssym(self, H: Union[List[float], List[int], np.ndarray]) -> float:
        """Retrieve the asymmetry angle eta

        Args:
            H (Union[List[float],List[int],np.ndarray): The reflecting plane of interest.

        Returns:
            float: the asymmetry angle

        Raises:
            TypeError: input must be 3x1 array
        """
        H = check3D(H)
        Hnorm = np.linalg.norm(H)

        Hz_prod = -np.dot(H, self.cryst.z_Surf())/Hnorm
        if np.abs(np.abs(Hz_prod)-1) < 1E-12:
            eta = 0.
        else:
            eta = np.arccos(-np.dot(H, self.cryst.z_Surf())/Hnorm)

        return eta

    def getAngles(self,  H: Union[List[float], List[int], np.ndarray],  Kin: Union[List[float], List[int], np.ndarray] = np.array([0, 0, 1])) -> List[float]:
        """Retrieve the principal angles of reflection 

        Args:
            H (Union[List[float],List[int],np.ndarray): The reflecting plane of interest.
            Kin (Union[List[float],List[int],np.ndarray], optional): The incoming photon ray in lab coordinates. Defaults to np.array([0,0,1]).

        Returns:
            Theta (float): angle of incidence of Kin towards H in radians
            Phi (float):  azimuthal angle between Kin and H in radians
            eta (float): asymmetry angle between H and surface
        Raises:
            TypeError: inputs must be 3x1 arrays
        """
        H = check3D(H)
        Kin = check3D(Kin)
        Hnorm = np.linalg.norm(H)
        Knorm = np.linalg.norm(Kin)
        K_H = self.cryst.R_Lab2H@Kin
        Kscalar = np.dot(K_H, H)/(Hnorm*Knorm)

        if Kscalar > 0:  # the formalism is based on negative valued K
            H = -H
            Kscalar = -Kscalar
        if np.abs(Kscalar+1) < 1E-12:
            Theta = np.pi/2
        else:
            Theta = np.arcsin(-Kscalar)

        eta = self.getAssym(H)

        if(np.abs(Theta-np.pi/2) <= 1E-12):
            Phi = 0  # ambigous
        else:
            xH = np.ndarray(3, dtype=float)
            yH = np.ndarray(3, dtype=float)
            if eta != 0:
                yH = normalize(np.cross(H, self.cryst.z_Surf()))
                xH = np.cross(yH, H)/Hnorm
            else:  # xH and yH are abitrary vectors perpendicular to H and, hence, zSurf
                xH = self.cryst.x()
                yH = self.cryst.y()
            ydummy = np.dot(yH, K_H)/(Knorm*np.cos(Theta))
            xdummy = np.dot(xH, K_H)/(Knorm*np.cos(Theta))

            Phi = np.arctan2(ydummy, xdummy)

        return [Theta, Phi, eta]

    def getAnglesOut(self,  H: Union[List[float], List[int], np.ndarray], E: float = None,
    wCorr:bool = True,  Kin: Union[List[float], List[int], np.ndarray] = None) -> List[float]:
        """Retrieve the angles after reflection

        Args:
            H (Union[List[float],List[int],np.ndarray): The reflecting plane of interest.
            E (float): The photon energy. If None, is taken as E_c. Defaults to None.
            wCorr (bool): If the refraction correction shall be applied. Defaults to true
            Kin (Union[List[float],List[int],np.ndarray], optional): The incoming photon ray in lab coordinates. If None, take the default Kin_Lab. Defaults to None.

        Returns:
            Theta_out (float): reflection angle of K_out towards H in radians
            Phi_out (float):  azimuthal angle between K_out and H in radians
        Raises:
            TypeError: inputs must be 3x1 arrays
        """
        H = check3D(H)
        if np.size(Kin)==1 and Kin==None:
            Kin = self.KInLab
        else:
            Kin = make_nparray(Kin)
            check3D(Kin)       
        if E==None:
            E = self.E_c
        Hnorm = 2*np.pi*np.linalg.norm(H)/self.a0
        Knorm = 2*np.pi*E/(Constants.h_planck_eV*Constants.c0)

        Theta_in, Phi_in, eta = self.getAngles(H,Kin)

        Delta_H = 0
        if wCorr:
            Delta_H = self.getDeltaH(E,H)

        #rounding errors
        Theta_out = Theta_in if eta==0 else np.real(np.abs(np.arcsin(-np.sin(Theta_in)+ Hnorm/Knorm - Delta_H*np.cos(eta)/Knorm)))
        x = np.cos(Theta_in)*np.cos(Phi_in) + Delta_H*np.sin(eta)/Knorm
        y = np.cos(Theta_in)*np.sin(Phi_in)

        Phi_out = 0 if np.abs(Theta_in-np.pi/2)<1E-10 else np.arctan2(y,x)[0]

        return [Theta_out, Phi_out]


    def getKH(self,H: Union[List[float], List[int], np.ndarray]=None, E: float = None, Theta_out:float=None, Phi_out:float=None) -> np.ndarray: 
        """return the direction vector in vacuum after reflection at plane H and energy E in lab-coordinates.

        Args:
            H (Union[List[float],List[int],np.ndarray): The reflecting plane of interest.
            E (float): The photon energy. If None, is taken as E_c. Defaults to None.
            Theta_out (float, optional): reflection angle of K_out towards H in radians. If None, calculate along with Phi_out (including correction). Defaults to None.
            Phi_out (float, optional): azimuthal angle between K_out and H in radians. If None, calculate along with Theta_out (including correction). Defaults to None.

        Returns:
            np.ndarray: the 3x1 direction vector 
        """
        H = check3D(H)
        if E==None:
            E = self.E_c
        if np.any(np.array([Theta_out,Phi_out])==None):
            Theta_out, Phi_out = self.getAnglesOut(H,E)
        eta = self.getAssym(H)

        Kout_Hspecific = np.array([np.cos(Theta_out)*np.cos(Phi_out),np.cos(Theta_out)*np.sin(Phi_out),np.sin(Theta_out)])

        #convert to coordinate system common to all H
        if eta != 0:
            yH = normalize(np.cross(H, self.cryst.z_Surf()))
            xH = np.cross(yH, H)/np.linalg.norm(H)
        else:  # xH and yH are abitrary vectors perpendicular to H and, hence, zSurf
            xH = self.cryst.x()
            yH = self.cryst.y()
        
        RHsT = np.array([xH,yH,H/np.linalg.norm(H)]).transpose()

        Kout_H = (RHsT@Kout_Hspecific).squeeze()


        return self.cryst.R_H2Lab@Kout_H

    def initialize(self):
        """initialize some important base parameters of the Bragg mirror for speeding up later calculations
        """

        self.cryst.calc_RLab2Cryst()

        # get the input angles (incoming nominal ray has direction [0,0,1])
        [self.Theta, self.Phi, self.eta] = self.getAngles(self.H0, self.KInLab)

        self.polarization2Beam()
        # direction cosines
        self.gamma0, self.gammaH = bmirror.dir_cos(
            self.Theta, self.Phi, self.eta)

        self.b_a = self.gamma0/self.gammaH  # asymmetry fector

        self.a0 = self.cryst.get_lattice_spacing(self.cryst.Tbase)
        self.dH0 = self.a0/np.linalg.norm(self.H0)
        self.Hnorm0 = 2*np.pi/self.dH0

        self.lambda_c, self.E_c = self.bragg_wavelength()

        self.bandwidth = self.getBandwidth()

    def polarization2Beam(self):
        """define the (two beam case specific) polarization directions and fractions for the base plane H0
        """
        KinH = self.cryst.R_Lab2H@self.KInLab
        # the polarization direction ([1,0,0] in Lab coords) in H_coords
        pol_in = self.cryst.R_Lab2H@self.polInLab
        if (np.abs(self.Theta-np.pi/2) > 1.E-6):  # Kin not perpendicular to surface
            self.sigma_pol = normalize(np.cross(self.H0, KinH))
        else:  # just take the incoming polarization as sigma_pol
            self.sigma_pol = pol_in
        self.pi_pol = np.cross(KinH, self.sigma_pol)
        self.sigma_pol_frac = np.dot(pol_in, self.sigma_pol)
        self.pi_pol_frac = np.dot(pol_in, self.pi_pol)

    def dir_cos(Theta: float, Phi: float, eta: float) -> List[float]:
        """return the direction cosines of incoming and reflected ray (approximated) for a given set of angles

        Args:
            Theta (float): Bragg angle
            Phi (float): azimuthal angle
            eta (float): asymmetry angle

        Returns:
            gamma0 (float): direction cosine of incoming ray
            gammaH (float): direction cosine of reflected ray (approximated, without deviation parameter)
        """
        gamma0 = np.cos(Theta)*np.sin(eta)*np.cos(Phi) + \
            np.sin(Theta)*np.cos(eta)
        # direction cosine of reflected ray (without small deviation parameter)
        gammaH = np.cos(Theta)*np.sin(eta)*np.cos(Phi) - \
            np.sin(Theta)*np.cos(eta)

        return [gamma0, gammaH]

    def bragg_wavelength(self, exact: bool = True, H=None) -> List[float]:
        """get the Bragg resonant wavelength

        Args:
            exact (bool, optional): if the refraction related small deviation shall be accounted for. Defaults to True.
            H: the reflection plane of interest. If None defaults to the principal reflection plane H0

        Returns:
            lambda : The wavelength at which the (modified) bragg condition is fullfilled
            E: The corresponding photon energy
        """
        if np.size(H)==1 and H==None:
            H = self.H0
        Theta, Phi, eta = self.getAngles(H, self.KInLab)
        dH = self.a0/np.linalg.norm(H)
        gamma0 = np.cos(Theta)*np.sin(eta)*np.cos(Phi) + \
            np.sin(Theta)*np.cos(eta)
        if(Theta==0):
            return [0, np.inf]
        
        lambda_Bragg = 2*np.sin(Theta)*dH
        
        E_Bragg = Constants.h_planck_eV*Constants.c0/lambda_Bragg

        if not exact:
            return [lambda_Bragg, E_Bragg]
        else:
            cp0 = self.cryst.getChi(E_Bragg, H, self.cryst.Tbase).squeeze()

            wH = -2*cp0[0].real*dH
            lambda_c = lambda_Bragg - wH*np.cos(eta)/(2*gamma0)
            E_c = Constants.h_planck_eV*Constants.c0/lambda_c

            return [lambda_c, E_c]

    def getBandwidth(self, H=None) -> np.ndarray:
        """get the approximative bandwidth in eV for reflection at plane H.
        Defaults to the plane H0.

        Args:
            H ([type], optional): The reflecting plane of interest. If None, defaults to the principal reflection plane H0. Defaults to None.

        Returns:
            List[float]: the bandwidth in eV (E_min, E_max)
        """
        mult_factor = 3  # a factor to multiply the bandwidth of total reflection with, to also include the "side wings"
        if np.size(H)==1 and H == None:
            Theta = self.Theta
            eta = self.eta
            dH = self.dH0
            H = self.H0
            gamma0 = self.gamma0
            b_a = self.b_a
            lambda_, E = [self.lambda_c, self.E_c]
        else:
            [Theta, Phi, eta] = self.getAngles(H, self.KInLab)
            dH = self.a0/np.linalg.norm(H)
            gamma0, gammaH = bmirror.dir_cos(Theta, Phi, eta)
            b_a = gamma0/gammaH
            lambda_, E = self.bragg_wavelength(False, H)

        cp0 = self.cryst.getChi(E, H, self.cryst.Tbase).squeeze()
        if(self.twoBFlag):
            Bw = mult_factor*(-4)*(dH/lambda_)**2 * \
                np.abs(cp0[1])/np.sqrt(np.abs(b_a))*np.array([1, -1])
            if(self.cryst.is_strained):  # wider bandwidth for strained crystal
                """in good approximation this can be taken into account by the shift of the central ph. energy (proportional to the lattice spacing) for a given strain. 
                the maximum bandwidth can than be calculated by using the maximum and minimum strain"""
                strain_z = np.diff(self.cryst.disp_Z)/np.diff(self.cryst.Z)
                strain_min, strain_max = [strain_z.min(), strain_z.max()]
                Bw[0] += 2*(1/(1+strain_max)-1)
                Bw[1] += 2*(1/(1+strain_min)-1)
        else:
            print("approximative bandwidth calculation for n_beam case not yet included")
            Bw = None
        return Bw

    def getDeltaH(self,E:float=None,H:Union[List,np.ndarray]=None,Theta:float=None, Phi:float=None, eta:float=None,Kin=None) -> float:
        """return the momentum transfer occurring at the interface between material and vacuum parallel to the surface normal

        Args:
            E (float,optional): The photon energy. If None, is taken as E_c. Defaults to None.
            H (Union[List[float],List[int],np.ndarray, optional): The reflecting plane of interest.
            Theta (float, optional): The Bragg angle in radians. If None, calculate from geometry (along with Phi and eta). Defaults to None.
            Phi (float, optional): The azimuthal angle in radians. If None, calculate from geometry (along with Theta and eta). Defaults to None.
            eta (float, optional): The asymmetry angle in radians. If None, calculate from geometry (along with Theta and Phi). Defaults to None.

        Returns:
            float: The momentum transfer magnitude.
        """
        if E==None:
            E=self.E_c
        if np.size(H)==1 and H==None:
            H = self.H0
        else:
            H = make_nparray(H)
            check3D(H)
        if np.size(Kin)==1 and Kin==None:
            Kin = self.KInLab
        else:
            Kin = make_nparray(Kin)
            check3D(Kin)
        if np.any(np.array([Theta,Phi,eta])==None):
            Theta, Phi, eta = self.getAngles(H,Kin)
        gamma0, gammaH = bmirror.dir_cos(Theta,Phi,eta)
        Knorm = 2*np.pi*E/(Constants.h_planck_eV*Constants.c0)
        Hnorm = 2*np.pi*np.linalg.norm(H)/self.a0
        alphaH = Hnorm/Knorm*(Hnorm/Knorm - 2*np.sin(Theta))  # deviation parameter
        Delta_Hdummy = Knorm*np.array([-gammaH-np.sqrt(gammaH**2-alphaH),-gammaH+np.sqrt(gammaH**2-alphaH)])
        idx_min = np.argmin(np.abs(Delta_Hdummy))
        return Delta_Hdummy[idx_min]
        #approximation
        #return -Knorm*alphaH/(2*gammaH)

    def getResAngle(self,E:float,H:Union[List,np.ndarray]=None,
    pitch=None,roll:float=0.,yaw:float=0.,
    limits:Union[List[float],Tuple[float]]=None):
        """retrieve the angle at which plane H makes 
        a Bragg reflection at photon energy E. 
        Only one of the three macroscopic rotation angles 
        (pitch,roll,yaw) can be unambiguously retrieved. 
        This specific angle shall be set as None, while 
        the others must have specific values.

        Args:
            E (float): The photon energy of interest
            H (Union): The crystal plane of interest, if None use
            H0. Defaults to None.
            pitch ([type], optional): The pitch angle. If None is
            set as the angle to be retrieved. Defaults to None.
            roll (float, optional): The roll angle. If None is
            set as the angle to be retrieved. Defaults to 0..
            yaw (float, optional): The yaw angle. If None is
            set as the angle to be retrieved. Defaults to 0.
            limits: If the angular range is limited. Needs to 
            have two values [upper,lower] or None, if no limit is imposed. 
            Defaults to None.

            Return:
                Angle (float): Resonant angle
        """
        assert all([np.size(ang)==1 for ang in [pitch,roll,yaw]]), "Angles must be denoted as single points."
        NoneFlags = np.array([ang==None for ang in [pitch,roll,yaw]])
        assert NoneFlags.sum()==1, "Exactly one angle must be set as None and the others as single floats."
        limitFlag = False
        if limits!=None:
            assert np.size(limits)==2, "Limits must be specified by two values [upper,lower]!"
        if NoneFlags[0]:
            if limits==None:
                limits = [deg2rad(1),np.pi/2]
            pitch = np.arange(limits[0],limits[1],deg2rad(0.1))
            ang = pitch
            roll, yaw = [make_nparray(roll),make_nparray(yaw)]
        elif NoneFlags[1]:
            if limits==None:
                limits = [-0.95*np.pi/2,0.95*np.pi/2]
            roll = np.arange(limits[0],limits[1],deg2rad(0.1))
            ang = roll
            pitch, yaw = [make_nparray(pitch),make_nparray(yaw)]
        else:
            if limits==None:
                limits = [-0.95*np.pi/2,0.95*np.pi/2]
            yaw = np.arange(limits[0],limits[1],deg2rad(0.1))
            ang = yaw
            pitch, roll = [make_nparray(pitch),make_nparray(roll)]
        if np.size(H)==1 and H==None:
            H = self.H0
        else:
            H = make_nparray(H)
            check3D(H)
            
        N = [angI.size for angI in [yaw, roll, pitch]]

        Ntot = np.prod(N)

        P_orig, R_orig, Y_orig = [self.cryst.pitch,self.cryst.roll,self.cryst.yaw]

        E_ang = np.ndarray(Ntot,dtype=float)
    
        for Pidx, P in enumerate(pitch):
            self.cryst.pitch = P
            for Ridx, R in enumerate(roll):
                self.cryst.roll = R
                for Yidx, Y in enumerate(yaw):
                    self.cryst.yaw = Y
                    self.cryst.calc_RLab2Cryst()
                    idx = Yidx + Ridx*N[0] + Pidx*N[1]*N[0]

                    E_ang[idx] = self.bragg_wavelength(exact=False,H=H)[1][0]
    
        AngIdx = np.argmin(np.abs(E_ang-E))
        Pidx = int(AngIdx/(N[0]*N[1]))
        Ridx = int((AngIdx%(N[0]*N[1]))/N[0])
        Yidx = (AngIdx%(N[0]*N[1]))%N[0]

        if np.abs(E_ang[AngIdx]/E -1) > 1E-2:
            self.cryst.pitch,self.cryst.roll,self.cryst.yaw = [P_orig,R_orig,Y_orig]
            self.cryst.calc_RLab2Cryst()
            return None #H has no reflection at E

        #for exact value do a fast optimization
        def opt_func(angFit,angArg,Edes):
            angsFit = np.ndarray(3,dtype=float)
            angsFit[NoneFlags] = angFit
            angsFit[~NoneFlags] = angArg

            self.cryst.pitch, self.cryst.roll, self.cryst.yaw = angsFit
            self.cryst.calc_RLab2Cryst()
            E_ang = self.bragg_wavelength(H=H)[1][0]
            return np.abs(Edes-E_ang)
        
        angs = np.array([pitch[Pidx],roll[Ridx],yaw[Yidx]])
        ang0 = angs[NoneFlags]
        angArg = angs[~NoneFlags]

        fitLimit = [0.,0.]
        fitLimit[0] = ang[AngIdx-1] if AngIdx!=0 else limits[0]
        fitLimit[1] = ang[AngIdx+1] if AngIdx!=(Ntot-1) else limits[1]
        

        optRes = opt.minimize(opt_func,ang0,args=(angArg,E),bounds=[(fitLimit[0],fitLimit[1])])
        self.cryst.pitch,self.cryst.roll,self.cryst.yaw = [P_orig,R_orig,Y_orig]
        self.cryst.calc_RLab2Cryst()

        return optRes.x


                    




    def getHplanes(self, E: Union[float, Tuple[float]], pitch: float = None, roll: float = None, yaw: float = None, wPlot:bool = False, savePlot:str = None) -> np.ndarray:
        """get the crystal planes participating in a 
        reflection at energy E for either the preconfigured 
        macroscopic orientation or a dedicated one as 
        specified by any or all of (pitch,roll,yaw).
        If angle is set, will fall back to original orientation
        afterwards

        A rather stupid routine, which just loops over a big set
        of possible planes
        Args:
            E (float, Tuple(float,float)): The photon energy or photon energy range in eV
            pitch (float, optional): The crystal pitch angle in radians. 
            If None, use preconfigured. Defaults to none.
            roll (float, optional): Same for roll angle. Defaults to none.
            yaw (float, optional): Same for yaw angle. Defaults to none.
            wPlot (bool, optional): If the orientation of the reflected rays shall be plotted. Defaults to False.
            savePlot (str, optional): If the plot shall be saved in a file with name "SavePlot". Defaults to None, meaning no saving.

        Returns:
            np.ndarray: [description]
        """
        if np.size(E)==1:
            lambda0 = Constants.h_planck_eV*Constants.c0/E
            lambda_range = np.array([lambda0[0]*(1-1E-3),lambda0[0]*(1+1E-3)])
            Erange = Constants.h_planck_eV*Constants.c0*1/lambda_range[::-1]
        elif np.size(E)==2:
            Erange = np.sort(make_nparray(E))
            lambda_range = Constants.h_planck_eV*Constants.c0*1/Erange[::-1]
        useBackup = False
        if any(np.array([pitch, roll, yaw]) != None):
            pitch_backup, roll_backup, yaw_backup = [
                self.cryst.pitch, self.cryst.roll, self.cryst.yaw]
            pitch_tmp = pitch if pitch != None else self.cryst.pitch
            roll_tmp = roll if roll != None else self.cryst.roll
            yaw_tmp = roll if roll != None else self.cryst.yaw
            self.cryst.pitch, self.cryst.roll, self.cryst.yaw = [
                pitch_tmp, roll_tmp, yaw_tmp]
            self.cryst.calc_RLab2Cryst(self)
            useBackup = True
        K_H = self.cryst.R_Lab2H@self.KInLab
        Hplane = []
        #i = 0
        #repeated_bool = True
        #limits = 10<
        # for n1 in range(-limits, limits):
        #     for n2 in range(-limits, limits):
        #         for n3 in range(-limits, limits):
        #             HPlaneDummy = np.array([n1, n2, n3])
        #             if np.dot(HPlaneDummy, K_H) > 0:
        #                 HPlaneDummy = HPlaneDummy*(-1)
        #             if (
        #                 any(HPlaneDummy != 0) and (
        #                     all(np.mod(HPlaneDummy, 2) == 1) or (
        #                         all(np.mod(HPlaneDummy, 2) == 0) and np.mod(np.sum(HPlaneDummy), 4) == 0)
        #                 )
        #             ):
        #                 lambdaB, EB = self.bragg_wavelength(exact=False,H=HPlaneDummy)
        #                 #if(lambdaB == 0): print(HPlaneDummy,lambdaB,EB)
        #                 if lambdaB > lambda_range[0] and lambdaB < lambda_range[1]:
        #                     for i_test in range(i):
        #                         if repeated_bool and all(Hplane[i_test] == HPlaneDummy):
        #                             repeated_bool = False
        #                     if repeated_bool:
        #                         Hplane.append(HPlaneDummy)
        #                         i = i+1
        #                     else:
        #
        #                          repeated_bool = True
        df_HplanesSub = self.df_Hplanes[self.df_Hplanes["E_B_min"]<Erange[1]]
        for HPlaneDummy in df_HplanesSub['hkl']:
            if np.dot(HPlaneDummy, K_H) > 0:
                HPlaneDummy = HPlaneDummy*(-1)
            lambdaB, EB = self.bragg_wavelength(exact=False,H=HPlaneDummy)
            if lambdaB > lambda_range[0] and lambdaB < lambda_range[1]:
                Hplane.append(HPlaneDummy)

        if wPlot or savePlot:
            fig = plt.figure(figsize=(12,8))
            ax2D = fig.add_subplot(121)
            ax3D = fig.add_subplot(122,projection='3d')

            ax2D.tick_params(labelsize=28)
            ax3D.tick_params(labelsize=28)

            rect = np.array([np.array(([-1, -1, 1, 1]))*0.1, np.array([-1, 1, 1, -1])*0.2, [0,0,0,0]])
            #rotation matrix for getting the right view
            Rrot = Rot_gen(np.pi,u = np.array([0,0,1]))@Rot_gen(np.pi/2,u = np.array([1,0,0]))
            rect = (Rrot@self.cryst.R_cryst2lab@rect).transpose()

            ax2D.plot(rect[:,1],rect[:,2],color='red',alpha=0.7)
            poly3D = mplot3d.art3d.Poly3DCollection([rect],facecolor="red",edgecolor="grey",alpha=0.7)
            ax3D.add_collection(poly3D)

            ax2D.arrow(-1,0,1,0,color='black',linewidth=2,ls='--',width=0.005,head_width=0.05,
            length_includes_head=True)
            ax2D.arrow(0,0,1,0,color='black',linewidth=2,ls='--',width=0.005,head_width=0.05,
            length_includes_head=True,label='Trans.')
            #ax2D.annotate("",xy=(0,0),xytext=(-1,0),arrowprops=dict(width=1,color='black',linestyle='--'))
            ax3D.quiver3D(0,-1,0,0,1,0,color='black',linewidth=2,ls='--')
            ax3D.quiver3D(0,0,0,0,1,0,color='black',linewidth=2,ls='--')
            #KHall = []
            for idx,H in enumerate(Hplane):
                KH = self.getKH(H,E).flatten()
                #KHall.append(KH)
                ax2D.arrow(x=0,y=0,dx=KH[2],dy=KH[1],width=0.005,head_width=0.05,length_includes_head=True,edgecolor=None,color=colors[idx],label=H.__str__())
                ax3D.quiver3D(0,0,0,-KH[0],KH[2],KH[1],linewidth=1.5,color=colors[idx])

            ax2D.set_xlim(-1,1)
            ax2D.set_ylim(-1,1)

            ax3D.set_xlim(-1,1)
            ax3D.set_ylim(-1,1)
            ax3D.set_zlim(-1,1)
            xticks = ax3D.get_xticks()
            ax3D.view_init(20,-25) 


            xlim = ax3D.get_xlim()
            xticks = np.linspace(xlim[0],xlim[1],3)

            ax3D.set_xticklabels(["{:2.0f}".format(-1*tick) for tick in xticks])
            ax3D.set_xticks(xticks)

            ax2D.set_xlabel("z",fontsize=32)
            ax2D.set_ylabel("y",fontsize=32)

            ax3D.set_xlabel("\nx",fontsize=32,linespacing=1)
            #ax3D.xaxis.set_label_coords(0,-1000) 

            ax3D.set_ylabel("\nz",fontsize=32,linespacing=1)
            ax3D.set_zlabel("\ny",fontsize=32)
            #ax3D.voxels(rect, facecolors='red', edgecolors='grey')  
            ax2D.legend(ncol=4,loc='lower left',bbox_to_anchor = (0,1,2.2,0.2),fontsize=24,
            borderaxespad=0.05,borderpad=0.2,columnspacing=0.5,handlelength=1.5,mode="expand") 
            if wPlot:
                plt.show()
            if savePlot:
                fig.savefig(savePlot,dpi=160)
            
            plt.close()
        return np.array(Hplane)

    def calcRefl_TB_wlext(self, E: Union[float, np.ndarray], K1: Union[List, np.ndarray] = None, makePlots: bool = False, ax: matplotlib.axes = None, savePlot:str = None) -> List[np.ndarray]:
        """Calculates the reflection/transmission-coefficient(s) and extinction length(s) of a specific bragg-mirror for (a) specific energy/ies E and a specific input ray K1 (in lab coordinates)  

        The function relies on the simplified two beam approximation. Also polarization terms are unified into the same reflection term (no polarization dependent tracking)

        Args:
            E (Union[float,np.ndarray]): The photon energy/ies of interest
            K1 (Union[List,np.ndarray]): The incoming photon ray in lab-coordinates. If None, just take the principal Kin. Defaults to None
            makePlots (bool): If the results shall be plotted
            axes (matplotlib.axes): If not equal None, the results will be plotted in the specific axes (even if makePlots = False). Defaults to None.
            savePlot (str, optional): If the plot shall be saved in a file with name "SavePlot". Defaults to None, meaning no saving.

        Returns:
            r0H: the complex reflection coefficient(s)
            t0H: the complex transmission coefficient(s)
            l_ext: the penetration depth(s)
        """
        if(K1 != None):
            K1 = check3D(K1)
        E = make_nparray(E)
        Knorm = 2*np.pi*E/(Constants.c0*Constants.h_planck_eV)

        P_sigma = 1.
        P_pi = np.cos(2*self.Theta)

        Hdummy = self.H0.copy()

        if np.size(K1)==1 and K1 == None:
            K1 = self.KInLab
        
        Theta, Phi, eta = self.getAngles(Hdummy, K1)
        gamma0, gammaH = bmirror.dir_cos(Theta, Phi, eta)
        b_a = gamma0/gammaH

        # set up polarization independent parameters

        alphaH = self.Hnorm0/Knorm - 2*np.sin(Theta)  # deviation parameter
        # correct gammaH
        gammaH = gammaH - alphaH*np.cos(eta)

        alphaH = alphaH*self.Hnorm0/Knorm

        # susceptibilities (transpose for faster access)
        cp = self.cryst.getChi(E, Hdummy, self.cryst.Tbase).transpose()

        # parameter for calculating the eigenvalues
        a_tilde = 0.5*(alphaH*b_a + cp[0, :]*(1-b_a))

        l_ext = 0
        if np.abs(self.sigma_pol_frac) > np.abs(self.pi_pol_frac):
            Ptmp = P_sigma
            Ptmp2 = P_pi
            Pmp = np.sqrt(1-self.pi_pol_frac*self.pi_pol_frac)
            pol_idx = [0,1]
        else:
            Ptmp = P_pi
            Ptmp2 = P_sigma
            Pmp = np.sqrt(1-self.sigma_pol_frac*self.sigma_pol_frac)
            pol_idx = [1,0]
        # if radiation is purely pi or sigma-polarized, then only one loop turn necessary
        iend = 1 if np.abs(Pmp - 1) < 0.001 else 2
        refl, trans, l_ext = [np.zeros([2,E.size],dtype=complex), np.zeros([2,E.size],dtype=complex),np.zeros([2,E.size],dtype=float)]
        #refl, trans = [0 + 0j, 0 + 0j]
        for i in range(iend):
            eps_1 = cp[0, :] - a_tilde + \
                np.sqrt(a_tilde**2 + b_a*Ptmp**2*cp[1, :]*np.conj(cp[1, :]))
            eps_2 = cp[0, :] - a_tilde - \
                np.sqrt(a_tilde**2 + b_a*Ptmp**2*cp[1, :]*np.conj(cp[1, :]))

            xi_1 = eps_1*Knorm/(2*gamma0)
            xi_2 = eps_2*Knorm/(2*gamma0)

            R_1 = (eps_1 - cp[0, :])/(Ptmp*cp[1, :])
            R_2 = (eps_2 - cp[0, :])/(Ptmp*cp[1, :])
            if(b_a<0):
                devisor = R_2 - R_1*np.exp(1j*(xi_1 - xi_2)*self.cryst.thickness)
                if np.abs(Ptmp)>1E-6:
                    refl[pol_idx[i]] += R_1*R_2*(
                        1. - np.exp(1j*(xi_1 - xi_2)*self.cryst.thickness)
                    )/devisor

                trans[pol_idx[i]] += (R_2-R_1)*np.exp(1j*xi_1*self.cryst.thickness)/devisor
            else:
                devisor = R_1-R_2
                if np.abs(Ptmp)>1E-6:
                    refl[pol_idx[i]] += R_1*R_2*(np.exp(1j*xi_2*self.cryst.thickness)-np.exp(1j*xi_1*self.cryst.thickness))/devisor
                trans[pol_idx[i]] += (R_1*np.exp(1j*xi_2*self.cryst.thickness)-R_2*np.exp(1j*xi_1*self.cryst.thickness))/devisor

            l_ext[pol_idx[i]] += np.abs(1/np.imag(xi_1-xi_2))
            #else:
            #    l_ext += Pmp*np.abs(1/np.imag(cp[0, :]))

            Pmp = np.sqrt(1-Pmp**2)
            Ptmp = Ptmp2

        if makePlots or ax!=None or savePlot:
            if ax == None:
                (fig, ax) = plt.subplots(figsize=(7.7, 5.5),tight_layout=True) #gridspec_kw=dict(left=0.195500133808642, bottom=0.2366666666666667, right=0.9172640615586418, top= 0.9045370370370371))
            else:
                fig = ax[0].get_figure()
            colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

            Trans_tot = np.abs(trans[0,:])**2+np.abs(trans[1,:])**2
            Refl_tot = np.abs(refl[0,:])**2+np.abs(refl[1,:])**2
            dE = (E-self.E_c)*1E3
            ax.plot(dE, Refl_tot/np.abs(b_a), linewidth=2.5, label="Reflectivity",color=colors[2])
            ax.plot(dE, Trans_tot, linewidth=2.5, label="Transm.",color=colors[1])
            ax.tick_params(labelsize=28)
            ax.grid()
            ax.set_xlim(dE[0], dE[-1])
            ax.set_ylim(0, 1)
            x_pos = 1.05
            y_pos = -0.145
            ax.set_xlabel('$\Delta E$ [meV]', fontsize=32)
            horizontalalignment = 'right'
            verticalalignment = 'top'
            offset_text = "+"+str(np.round(self.E_c*1E-3, 2))+"keV"
            ax.text(x_pos, y_pos, offset_text, transform=ax.transAxes,
                    horizontalalignment=horizontalalignment,
                    verticalalignment=verticalalignment, fontsize=26)
            #ax.set_title("Reflection at " + Hdummy.__str__() + " plane", fontsize=32)
            lh = ax.legend(shadow=True, fontsize=28, bbox_to_anchor=(1.05, 1.05), loc='upper right',
                           borderaxespad=0., title="plane " + Hdummy.__str__(), title_fontsize=28, handlelength=1.2, borderpad=0.1, handletextpad=0.3)
            if makePlots or ax!=None:
                plt.show()
            if savePlot:
                fig.savefig(savePlot,dpi=160)

        return [refl, trans, l_ext]

    def calcRefl_TB(self, E: Union[float, np.ndarray], K1: Union[List, np.ndarray] = None, wlext=False, pol_comp: bool = False, makePlots: bool = False, ax: matplotlib.axes = None, savePlot:str = None) -> List[np.ndarray]:
        """Calculates the reflection/transmission-coefficient(s) of a specific bragg-mirror for (a) specific energy/ies E and a specific input ray K1 (in lab coordinates)  

        The function relies on the simplified two beam approximation. Also polarization terms are unified into the same reflection term (no polarization dependent tracking)

        This function is a wrapper for the more general :func:`~bmirror.bmirror.calcRefl_TB_wlext` but only returning the usually not required extinction length if demanded

        Args:
            E (Union[float,np.ndarray]): The photon energy/ies of interest
            K1 (Union[List,np.ndarray]): The incoming photon ray in lab-coordinates. If None, just take the principal Kin. Defaults to None
            wlext (bool): only return the extinction length if required. Defaults to False.
            pol_comp (bool): If the results shall be returned per polarization component --> If True, r0H and t0H becomes (2xNHxlength(E)) arrays with the first row corresponding to sigma_pol and the second to pi_pol. If False, only the reflection along the initial polarization is returned.
            makePlots (bool): If the results shall be plotted
            axes (matplotlib.axes): If not equal None, the results will be plotted in the specific axes (even if makePlots = False). Defaults to None.
            savePlot (str, optional): If the plot shall be saved in a file with name "SavePlot". Defaults to None, meaning no saving.

        Returns:
            r0H: the complex reflection coefficient(s)
            t0H: the complex transmission coefficient(s)
            l_ext: the penetration depth(s), optional
        """
        refl, trans, l_ext = self.calcRefl_TB_wlext(E, K1,makePlots,ax,savePlot)
        if not pol_comp:
            refl = self.sigma_pol_frac*refl[0,:]+self.pi_pol_frac*refl[1,:]
            trans = self.sigma_pol_frac*trans[0,:]+self.pi_pol_frac*trans[1,:]
            l_ext = self.sigma_pol_frac*l_ext[0,:]+self.pi_pol_frac*l_ext[1,:]
        if wlext:
            return [refl, trans, l_ext]
        else:
            return [refl, trans]

    def calcRefl_TB_strained(self, E: Union[float, np.ndarray], x: float, y: float, K1: Union[List, np.ndarray] = None) -> List[np.ndarray]:
        """(to be implemented in the near future!) reflectivity of a three(two) dimensionally strained crystal in the two beam approx at (a) energy/ies E and surface position (x,y)

        Args:
            E (Union[float,np.ndarray]): The photon energy/ies of interest
            x (float): The x-coordinate on the crystal surface in m
            y (float): The y-coordinate on the crystal surface in m
            K1 (Union[List,np.ndarray]): The incoming photon ray in lab-coordinates. If None, just take the principal Kin. Defaults to None


        Returns:
            r0H: the complex reflection coefficient(s)
            t0H: the complex transmission coefficient(s)
            l_ext: the penetration depth(s)

        This function basically only wraps subfunction for the more specific cases, for example for the case of a 2D strain and symmetric reflection etc. 
        Each specification makes a significant speed up possible
        TODO: No strained crystal reflection implemented yet!
        """
        raise AssertionError("No strained crystal reflection implemented yet!")

    def calcRefl(self, E: Union[float, np.ndarray], x: float = None, y: float = None, wlext=False, pol_comp: bool = False, makePlots: bool = False, ax: matplotlib.axes = None, savePlot:str = None) -> List[np.ndarray]:
        """an interface for the diffraction calculation. 
          Depending on the bmirror configuration (if two beam case, strained crystal, ...) decides for the appropriate subroutines to calculate the reflection/transmission coefficients

        Args:
            E (Union[float,np.ndarray]): The photon energy/ies of interest
            x (float): if crystal not strained, corresponds to the x-component of the photon beam direction (in absolute of the wavenumber), else corresponds to the  x-coordinate on the crystal surface in m. If none, take default input direction/surface position (0,0)
            y (float): Same for the y-coordinate
            wlext (bool): only return the extinction length if required. Defaults to False.
            pol_comp (bool): If the results shall be returned per polarization component --> If True, r0H and t0H becomes (2xNHxlength(E)) arrays with the first row corresponding to sigma_pol and the second to pi_pol 
            makePlots (bool): If the results shall be plotted
            axes (matplotlib.axes): If not equal None, the results will be plotted in the specific axes (even if makePlots = False). Defaults to None.
            savePlot (str, optional): If the plot shall be saved in a file with name "SavePlot". Defaults to None, meaning no saving.

        Returns:
            r0H: the complex reflection coefficient(s)
            t0H: the complex transmission coefficient(s)
        """
        if self.twoBFlag:
            if self.cryst.isstrained:
                return self.calcRefl_TB_strained(E,x,y)
            else:
                if x == None and y == None:
                    Kin = self.KInLab
                else:
                    Knorm = 2*np.pi*E/(Constants.h_planck_eV*Constants.c0)
                    x = 0 if x == None else x/Knorm
                    y = 0 if y == None else y/Knorm
                    Kin = np.array([x, y, np.sqrt(1-x**2-y**2)])
                return self.calcRefl_TB(E,Kin,wlext,pol_comp,makePlots,ax)

    def rockingCurve(self, pitch: Union[float,List,np.ndarray], roll: Union[float,List,np.ndarray]=None, yaw: Union[float,List,np.ndarray] = None, E: float=None, wlext=False, makePlots=False) -> List[np.ndarray]:
        """an interface for rocking curves at an energy E
            Depending on the bmirror configuration (if two beam case, strained crystal, ...) decides for the appropriate subroutines to calculate the reflection/transmission coefficients

        Args:
            pitch (Union[float,np.ndarray]): The pitch angles of interest. If None, use preconfigured
            roll (Union[float,np.ndarray]): The roll angles of interest.
            If None, use preconfigured. Defaults to None.
            yaw (Union[float,np.ndarray]): The yaw angles of interest.
            If None, use preconfigured. Defaults to None.
            E (float): The photon energy at which to run the rocking curve.
            If None, use E_c. Defaults to None.
            wlext (bool): only return the extinction length if required. Defaults to False.
            makePlots (bool): Whether to automatically make plots

        Returns:
            r0H: the complex reflection coefficient(s)
            t0H: the complex transmission coefficient(s)
            lext: The extinction length (optional)
        """
        if self.twoBFlag:
            if self.cryst.isstrained:
                return self.rockingCurve_TB_strained(pitch,roll,yaw,E,wlext)
            else:
                return self.rockingCurve_TB(pitch,roll,yaw,E,wlext,makePlots)

    def rockingCurve_TB(self, pitch: Union[float,List,np.ndarray], roll: Union[float,List,np.ndarray]=None, yaw: Union[float,List,np.ndarray] = None, E: float=None, wlext=False, makePlots:bool = False) -> List[np.ndarray]:
        """Calculates the rocking curve (reflection/transmission) of a specific bragg-mirror for at photon energy E for a range of angles (pitch,roll,yaw).


        Args:
            pitch (Union[float,np.ndarray]): The pitch angles of interest. If None, use preconfigured
            roll (Union[float,np.ndarray]): The roll angles of interest.
            If None, use preconfigured. Defaults to None.
            yaw (Union[float,np.ndarray]): The yaw angles of interest.
            If None, use preconfigured. Defaults to None.
            E (float): The photon energy at which to run the rocking curve.
            If None, use E_c. Defaults to None.
            wlext (bool): only return the extinction length if required. Defaults to False.

        Returns:
            r0H: the complex reflection coefficient(s)
            t0H: the complex transmission coefficient(s)
            lext: The extinction length (optional)
        """
        pitch_orig,roll_orig,yaw_orig = [self.cryst.pitch, self.cryst.roll, self.cryst.yaw]
        DimensionFlag = "0D"
        NoneFlags = np.array([np.size(ang)==1 and ang==None for ang in [pitch,roll,yaw]])
        if E==None:
            E = self.E_c

        if NoneFlags.sum()==0:
            DimensionFlag = "3D"
        elif sum(NoneFlags)==1: 
            DimensionFlag = "2D"
        elif sum(NoneFlags)==2: 
            DimensionFlag = "1D"
        if NoneFlags[0]:
            pitch = np.array([self.cryst.pitch])
            Npitch = 1
        else:
            pitch = make_nparray(pitch)
            Npitch = pitch.size
        if NoneFlags[1]:
            roll = np.array([self.cryst.roll])
            Nroll = 1
        else:
            roll = make_nparray(roll)
            Nroll = roll.size
        if NoneFlags[2]:
            yaw = np.array([self.cryst.yaw])
            Nyaw = 1
        else:
            yaw = make_nparray(yaw)
            Nyaw = yaw.size
        
        
        r0H = np.ndarray((Npitch,Nroll,Nyaw),dtype=complex)
        t00 = np.ndarray((Npitch,Nroll,Nyaw),dtype=complex)
        lext = np.ndarray((Npitch,Nroll,Nyaw),dtype=float)

        for ipitch, pitch_ in enumerate(pitch):
            self.cryst.pitch = pitch_
            for iroll, roll_ in enumerate(roll):
                self.cryst.roll = roll_
                for iyaw, yaw_ in enumerate(yaw):    
                    self.cryst.yaw = yaw_

                    self.cryst.calc_RLab2Cryst()
                    r0H_I, t00_I, lext_I =  self.calcRefl_TB(E,makePlots=False,wlext=True)
                    

                    r0H[ipitch,iroll,iyaw] = r0H_I[0]
                    t00[ipitch,iroll,iyaw] = t00_I[0]
                    lext[ipitch,iroll,iyaw] = lext_I[0]
        
        self.cryst.pitch,self.cryst.roll,self.cryst.yaw = [pitch_orig,roll_orig,yaw_orig]
        self.cryst.calc_RLab2Cryst()

        if makePlots:
            if DimensionFlag != "1D":
                print ("Can only produce plots for 1D problem.")
            else: 
                plotIdx = int(np.where(~NoneFlags)[0][0])
                ang = np.array([pitch-np.pi/2, roll, yaw],dtype=object)[plotIdx]
                AngLabel = np.array(["Pitch [mrad]", "Roll [mrad]", "Yaw [mrad]"])[plotIdx]

                fig, ax = plt.subplots(figsize=(7.7, 5.5),tight_layout=True) 
                ax.plot(ang*1E3,(np.abs(r0H)**2).squeeze(),linewidth=2.5)
                ax.tick_params(labelsize=28)
                ax.grid()
                ax.set_xlim(ang.min()*1E3, ang.max()*1E3)
                ax.set_ylim(0, 1)
                ax.set_xlabel(AngLabel, fontsize=32)

        if wlext:
            return [r0H, t00, lext]
        else:
            return [r0H, t00]



    def rockingCurve_TB_strained(self, pitch: Union[float,List,np.ndarray], roll: Union[float,List,np.ndarray]=None, yaw: Union[float,List,np.ndarray] = None, E: float=None, wlext=False) -> List[np.ndarray]:
        """Calculates the rocking curve (reflection/transmission) of a specific strained(!) bragg-mirror for at photon energy E for a range of angles (pitch,roll,yaw).

        TODO: Not yet implemented


        Args:
            pitch (Union[float,np.ndarray]): The pitch angles of interest. If None, use preconfigured
            roll (Union[float,np.ndarray]): The roll angles of interest.
            If None, use preconfigured. Defaults to None.
            yaw (Union[float,np.ndarray]): The yaw angles of interest.
            If None, use preconfigured. Defaults to None.
            E (float): The photon energy at which to run the rocking curve.
            If None, use E_c. Defaults to None.
            wlext (bool): only return the extinction length if required. Defaults to False.

        Returns:
            r0H: the complex reflection coefficient(s)
            t0H: the complex transmission coefficient(s)
            lext: The extinction length (optional)
        """
        raise AssertionError("No strained crystal reflection implemented yet!")


    def BraggCurvesEvsAngles_inRange(self, Erange: Tuple[float], PitchRange: Union[float,List,np.ndarray], RollRange: Union[float,List,np.ndarray]=None, YawRange: Union[float,List,np.ndarray] = None, hmax: int = None, kmax = None, lmax = None) -> List[np.ndarray]:
        """Retrieves the number of reflecting planes and their respective Bragg
        energies inside a defined energy and angular range. The angular range is sampled with 1000 points.



        Args:
            Erange (Tuple[float]): The upper and lower border of the photon energy to look for bragg reflections
            PitchRange (Union[float,List,np.ndarray]): The pitch angle of interest. If size>1, then the angular range in which too look for Bragg reflections.
            RollRange (Union[float,List,np.ndarray]): The roll angle of interest. If size>1, then the angular range in which too look for Bragg reflections. Defaults to None = the currently set roll angle.
            YawRange (Union[float,List,np.ndarray]): The yaw angle of interest. If size>1, then the angular range in which too look for Bragg reflections. Defaults to None = the currently set yaw angle.
            hmax, kmax, lmax (int): The maximum reflection order in hkl to look for. Defaults to None = no limit

        Returns:
            EBragg: the bragg energies for the reflecting planes inside the 
            defined range, for each angular sampling point 
            hkls: the hkl indices of the reflecting planes 
            pitch_sampling: the sampled pitch angles
            roll_sampling: the sampled roll angles
            yaw_sampling: the sampled yaw angles
        """

        Erange = np.sort(make_nparray(Erange))
        lambda_range = Constants.h_planck_eV*Constants.c0*1/Erange[::-1]
       
    
        pitch_backup, roll_backup, yaw_backup = [
            self.cryst.pitch, self.cryst.roll, self.cryst.yaw]

        df_HplanesSub = self.df_Hplanes[self.df_Hplanes["E_B_min"]<Erange[1]]
        for i, imax in zip(['h','k','l'],[hmax,kmax,lmax]):
            if imax != None:
                df_HplanesSub = df_HplanesSub[np.abs(df_HplanesSub[i])<imax]

        if PitchRange == None:
            PitchRange = make_nparray(self.cryst.pitch)
        else:
            PitchRange = make_nparray(PitchRange)
        if RollRange == None:
            RollRange = make_nparray(self.cryst.roll)
        else:
            RollRange = make_nparray(RollRange)
        if YawRange == None:
            YawRange = make_nparray(self.cryst.yaw)
        else:
            YawRange = make_nparray(YawRange)

        if (np.size(PitchRange)==1 and np.size(RollRange)==1 and np.size(YawRange)==1):
            raise AssertionError("At least one angle needs to be of size >=2. Otherwise use .get_Hplanes(...)")
        Pitch_Red, Roll_Red, Yaw_Red = [PitchRange,RollRange,YawRange]
        Pitch_sampling, Roll_sampling, Yaw_sampling = [PitchRange,RollRange,YawRange]
        numPreSampling = 20 #pre-sampling for reduced entries
        numSampling = 1000
        if np.size(PitchRange)>=2:
            Pitch_Red = np.linspace(np.min(PitchRange),np.max(PitchRange),numPreSampling)
            Pitch_sampling = np.linspace(np.min(PitchRange),np.max(PitchRange),numSampling)
        if np.size(RollRange)>=2:
            Roll_Red = np.linspace(np.min(RollRange),np.max(RollRange),numPreSampling)
            Roll_sampling = np.linspace(np.min(RollRange),np.max(RollRange),numSampling)
        if np.size(YawRange)>=2:
            Yaw_Red = np.linspace(np.min(YawRange),np.max(YawRange),numPreSampling)
            Yaw_sampling = np.linspace(np.min(RollRange),np.max(YawRange),numSampling)

        E_red = np.zeros([np.size(Yaw_Red), np.size(Roll_Red), np.size(Pitch_Red), df_HplanesSub.shape[0]],dtype=float)
        # E_min, E_max = np.zeros(df_HplanesSub.shape[0],dtype=float), np.zeros(df_HplanesSub.shape[0],dtype=float)
        try:
            for iY, YawI in enumerate(Yaw_Red):
                for iR, RollI in enumerate(Roll_Red):
                    for iP, PitchI in enumerate(Pitch_Red):
                        self.cryst.pitch, self.cryst.roll, self.cryst.yaw = [PitchI, RollI, YawI]
                        self.cryst.calc_RLab2Cryst()
                        K_H = self.cryst.R_Lab2H@self.KInLab
                        for iH,Hplane in enumerate(df_HplanesSub['hkl']):
                            if np.dot(Hplane, K_H) > 0:
                                Hplane = -1*Hplane
                            E_red[iY,iR,iP,iH] = self.bragg_wavelength(exact=False,H=Hplane)[1]
        except:
            #roll back
            self.cryst.pitch, self.cryst.roll, self.cryst.yaw = [
            pitch_backup, roll_backup, yaw_backup]
            self.cryst.calc_RLab2Cryst()
            raise RuntimeError("Some Problems in the routine occured.\nSwitching back to original angles.")

        #df_HplanesSub = df_HplanesSub[E_min>]           

        #E_H = np.zeros(Yaw_sampling.size, Roll_sampling.size, Pitch_sampling.size, df_HplanesSub.shape[0],dtype=float)
        bool_red = [np.logical_and(E.flatten()>Erange[0] ,E.flatten()<Erange[1]).any() for E in E_red.transpose()]
        df_HplanesSub = df_HplanesSub[bool_red]

        E_Bragg = np.zeros([Yaw_sampling.size, Roll_sampling.size, Pitch_sampling.size, df_HplanesSub.shape[0]],dtype=float)
        for iY, YawI in enumerate(Yaw_sampling):
                for iR, RollI in enumerate(Roll_sampling):
                    for iP, PitchI in enumerate(Pitch_sampling):
                        self.cryst.pitch, self.cryst.roll, self.cryst.yaw = [PitchI, RollI, YawI]
                        self.cryst.calc_RLab2Cryst()
                        K_H = self.cryst.R_Lab2H@self.KInLab                        
                        for iH,Hplane in enumerate(df_HplanesSub['hkl']):
                            if np.dot(Hplane, K_H) > 0:
                                Hplane = -1*Hplane
                            E_Bragg[iY,iR,iP,iH] = self.bragg_wavelength(exact=False,H=Hplane)[1]

        # roll back
        self.cryst.pitch, self.cryst.roll, self.cryst.yaw = [
            pitch_backup, roll_backup, yaw_backup]
        self.cryst.calc_RLab2Cryst()
        
        
        return E_Bragg.squeeze(), df_HplanesSub['hkl'].to_numpy(), Pitch_sampling, Roll_sampling, Yaw_sampling












        

"""cr = crystal("Si")
test1 = bmirror([1,0,0],cr)
test2 = bmirror([1,0,0],"Diamond")
print(test2.lambda_c)"""
