# Class with functions to analyse data from a RoentDek Hexanode detector #

# These functions expect files is the format of a .txt with entries like this in the lines:
# [How many triggers] [time passed] [number of hits] [particle 1 x] [particle 1 y] [particle 1 t] [particle 2 x] ...

import numpy as np
import pandas as pd

class hexanodeanalysis:

    #Read a .txt file which was created by reading a .ccf into Cobold and enabling this:
    #Parameter 1008,3
    #"Write data back to hard drive (0=no, 1=yes ASCII, 2=yes LMF, 3=ASCII special)"
	def readFromCoboldTxt(path,filename,info=False):

    if info == True:
        print("Function expects (path,filename) to a detector.txt with a certain format.\n\
        	  Funcion returns a dictionary with the following entries:\n\
        	  [shotno]\n\
        	  [timerel]\n\
        	  [hitno]\n\
        	  [p1] (x,y,t)\n\
        	  [p2] (x,y,t)\n\
        	  [p3] (x,y,t)\n\
        	  [p4] (x,y,t)"
        	  ) 

    readin = pd.read_csv(path+filename,sep=' ',header=None)

    ll = len(readin[0])
    
    data = {
        "shotno": np.empty(ll,dtype=int),
        "timerel":np.empty(ll,dtype=float),
        "hitno":np.empty(ll,dtype=int),
        "p1":np.empty((ll,3),dtype=float),
        "p2":np.empty((ll,3),dtype=float),
        "p3":np.empty((ll,3),dtype=float),
        "p4":np.empty((ll,3),dtype=float)
        }
    
    data["shotno"] = np.array(readin[0][:])
    data["timerel"] = np.array(readin[1][:])
    data["hitno"] = np.array(readin[2][:])
    data["p1"] = np.array([readin[3][:],readin[4][:],readin[5][:]])
    data["p2"] = np.array([readin[6][:],readin[7][:],readin[8][:]])
    data["p3"] = np.array([readin[9][:],readin[10][:],readin[11][:]])
    data["p4"] = np.array([readin[12][:],readin[13][:],readin[14][:]])
    
    return data


    #--------------------------------------------------------------------------------------#
    #Take data and return the times of all hits
    def getToF(data,info=False):

    if info == True:
    	print("This function takes the data in the dict format and gives out the times of\
    		  all the recorded hits in a list. Making a histogram out of this will yield\
    		  the time of flight spectrum.")

    times = np.zeros((ll*4,1),dtype=float)
    
    j = 0
    for i in range(ll):
        for prtcl in ["p1","p2","p3","p4"]:
            tof = data[prtcl][2][i]
            if tof > 1:
                times[j] = tof
                j += 1
    
    return times[:j]


    #--------------------------------------------------------------------------------------#
    #Takes the data and gives a list of [x,y] for every hit in a certain time window
	def xyfromToF(data,trange,info=False):

        if info == True:
        	print("Function expects dict data and a time of flight range of the mass over\
        		  charge ration which you want to get the spatial distribution from:\
        		  (data,trange).\n\
        		  The function returns a list of the xy coordinates of all particle in data\
        		  which meet the time of flight criterion.")

	    ll = data["shotno"].shape[0]
	    
	    elementhits = np.empty((ll,2),dtype=float)
	    
	    j = 0
	    for i in range(ll):
	        for prtcl in ["p1","p2","p3","p4"]:
	            if data[prtcl][2][i] > trange[0] and data[prtcl][2][i] < trange[1]:
	                elementhits[j] = [data[prtcl][0][i], data[prtcl][1][i]]
	                j += 1
	   
	    return elementhits[:j]



    #--------------------------------------------------------------------------------------#
    #Creates a square histogram from a list of [x,y] coordinates.
	def makeSquareHistogram(neg,pos,nbins,xydata,info=False):

		if info == True:
			print("This function takes a list of [x,y] coordinates and makes a 2d histogram.\
				   The function takes the minimum and maximum value you want to incorporate\
				   into your histogram and the number of bins.\n\
				   The function returns the xy histogram and the x and y edges.")

	    xbin = np.linspace(neg,pos,nbins+1)
	    ybin = np.linspace(neg,pos,nbins+1)
	    H,xedges,yedges = np.histogram2d(xydata[:,0],xydata[:,1],bins=(xbin,ybin))
	    return H.T,xedges,yedges






### What would be good to do with data:
### 1. Display a time of flight spectrum
### 2. Make a time dict for the mass/charge ratios you are interested in
### 3. Create the xy distributions of the mass/charge ratio you want to look at
### 4. Abel the images
### 5. Find center
### 6. radial integration