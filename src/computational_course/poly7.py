#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class poly7:
    def __init__(self, eps, sig, rcut, rpoly):
        
        self.A = ( (1/((rcut - rpoly)**7* rpoly**12))*4* eps* rcut**4* sig**6*
                 (2*rpoly**6 *(-42* rcut**3 + 182*rcut**2* rpoly -273* rcut* rpoly**2 +
          143* rpoly**3) + (455* rcut**3 - 1729*rcut**2* rpoly +
          2223* rcut* rpoly**2 - 969* rpoly**3)* sig**6) )
    
        self.B = ( (1/((rcut - rpoly)**7* rpoly**13))*16* eps* rcut**3* sig**6* 
                    (rpoly**6* (54* rcut**4 - 154* rcut**3* rpoly + 
          351* rcut *rpoly**3 - 286* rpoly**4) + (-315* rcut**4 + 749 *rcut**3 * rpoly + 
          171 *rcut**2* rpoly**2 - 1539* rcut* rpoly**3 + 969* rpoly**4)* sig**6) )
                                                
        self.C = ( (1/((rcut - rpoly)**7* rpoly**14))*12* eps* rcut**2* sig**6* 
          (rpoly**6* (-63* rcut**5 - 7* rcut**4 *rpoly + 665* rcut**3 *rpoly**2 - 
          975* rcut**2* rpoly**3 - 52* rcut* rpoly**4 + 572* rpoly**5) + 
          2 *(195* rcut**5 + 91* rcut**4* rpoly - 1781* rcut**3* rpoly**2 + 
          1995 *rcut**2* rpoly**3 + 399* rcut* rpoly**4 - 969* rpoly**5)* sig**6) )
              
        self.D = ( (1/((rcut - rpoly)**7* rpoly**15))*16* eps* sig**6* 
          (rcut* rpoly**6* (14* rcut**6 + 126* rcut**5* rpoly - 420* rcut**4* rpoly**2 
          -90* rcut**3* rpoly**3 + 1105* rcut**2* rpoly**4 - 624* rcut* rpoly**5 - 
          286 *rpoly**6) + rcut* (-91* rcut**6 - 819* rcut**5* rpoly + 2145 * 
          rcut**4 * rpoly**2 + 1125* rcut**3* rpoly**3 - 5035* rcut**2* rpoly**4 + 
          1881* rcut* rpoly**5 + 969* rpoly**6)* sig**6) )
                                 
        self.E = ( (1/((rcut - rpoly)**7* rpoly**15))*4* eps* sig**6* 
          (2* rpoly**6* (-112* rcut**6 - 63* rcut**5* rpoly + 1305* rcut**4* rpoly**2 
          -1625* rcut**3* rpoly**3 - 585* rcut**2* rpoly**4 + 
          1287 *rcut* rpoly**5 + 143* rpoly**6) + (1456*rcut**6 +1404*rcut**5* rpoly - 
          14580 *rcut**4* rpoly**2 + 13015* rcut**3* rpoly**3 + 7695* rcut**2* rpoly**4 - 
          8721 *rcut* rpoly**5 - 969* rpoly**6)* sig**6) )
                                                 
        self.F = ( (1/((rcut - rpoly)**7* rpoly**15))*48* eps* sig**6* 
          (-rpoly**6* (-28* rcut**5 + 63* rcut**4* rpoly + 65* rcut**3* rpoly**2 - 
          247* rcut**2* rpoly**3 + 117* rcut* rpoly**4 + 65* rpoly**5) + 
          (-182* rcut**5 + 312* rcut**4* rpoly + 475* rcut**3* rpoly**2 - 
          1140* rcut**2* rpoly**3 + 342* rcut* rpoly**4 + 228* rpoly**5)* sig**6) )
              
        self.G = ( (1/((rcut - rpoly)**7* rpoly**15))*4* eps* sig**6* (rpoly**6* 
          (-224* rcut**4 + 819* rcut**3* rpoly - 741* rcut**2* rpoly**2 
          -429* rcut* rpoly**3 + 715* rpoly**4) + 2 *(728* rcut**4 
          -2223* rcut**3* rpoly + 1425* rcut**2* rpoly**2 
          +1292* rcut* rpoly**3 - 1292* rpoly**4)* sig**6) )
                              
        self.H = ( (1/((rcut - rpoly)**7* rpoly**15))*16* eps* sig**6* (rpoly**6* 
          (14* rcut**3 - 63* rcut**2* rpoly + 99* rcut* rpoly**2 - 55* rpoly**3) + 
          (-91* rcut**3 + 351* rcut**2* rpoly - 459* rcut* rpoly**2 
          +204* rpoly**3)* sig**6) )
        
#functions calculating energy and forces could be put here as methods of the class poly7
    #def calcEpot(self, coords, numNbrs, idxNbrs):
    
     
    #def calcForces(self, coords, numNbrs, idxNbrs):