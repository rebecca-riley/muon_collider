#given cross-sections calculated from madgraph find the minimum luminosity given a coupling factor
import matplotlib.pyplot as plt
import numpy as np

#min number of events required for luminosity restriction (5 standard)
nEvents = 5

#create array of possible alpha values                    
#alpha is the ratio 1/(G_flambda^2), defined for brevity                                                    
alpha = np.array([0.001, 0.01, 0.1, 1])

###########

#Read input from user (!) later have this be input from another file. Probably call as function within get_pass_cuts.py
#Need two cross-sections for different coupling strengths (UNCUT) 

print "Note that in the following sigma_sig_1, sigma_sig_2, and sigma_sm are now the UNCUT values."
input_ = input("Input the following, in order, as a list. [alpha_1, alpha_2, sigma_sig_1, e_sig_1, f_sig_1, sigma_sig_2, e_sig_2, f_sig_2, sigma_sm, e_sm, f_sm] ")

print ""

alpha_1 = float(input_[0])
alpha_2 = float(input_[1])
sigma_sig_1 = float(input_[2])
e_sig_1 = float(input_[3])
f_sig_1 = float(input_[4])
sigma_sig_2 = float(input_[5])
e_sig_2 = float(input_[6])
f_sig_2 = float(input_[7])
sigma_sm = float(input_[8])
e_sm = float(input_[9])
f_sm = float(input_[10])

#-- Redefine values and errors to be "with cuts" --#

#Values
sigma_sig_1 = 0.01*f_sig_1*sigma_sig_1 #assumes fraction given as percent not decimal => 50 not 0.5
sigma_sig_2 = 0.01*f_sig_2*sigma_sig_2
sigma_sm = 0.01*f_sm*sigma_sm

#Errors
e_sig_1 = 0.01*f_sig_1*e_sig_1
e_sig_2 = 0.01*f_sig_2*e_sig_2
e_sm = 0.01*f_sm*e_sm

######################################
## calculate sigma_np and sigma_int ##
######################################

#Values
beta = alpha_2/alpha_1 

sigma_np = ((beta*sigma_sig_1 - sigma_sig_2) + (1-beta)*sigma_sm)/(beta*(alpha_1**2) - (alpha_2**2))
sigma_int = (sigma_sig_2 - sigma_sm - (alpha_2**2)*sigma_np)/(2*alpha_2)

#Errors
d = (beta*e_sig_1)/(beta*(alpha_1**2) - alpha_2**2)
g = -e_sig_2/(beta*(alpha_1**2) - alpha_2**2)
h = ((1-beta)*e_sm)/(beta*(alpha_1**2) - alpha_2**2)

e_np = np.sqrt( d**2 + g**2 + h**2 )

a = e_sig_2/(2.*alpha_2)
b = -e_sm/(2.*alpha_2)
c = -(alpha_2*e_np)/2.

e_int = np.sqrt( a**2 + b**2 + c**2 )

#Print results
print "sigma_np = ",sigma_np," +- ",e_np
print "sigma_int = ",sigma_int," +- ",e_int
print ""

#########################################
## calculate sigma_sig for given alpha ##
#########################################

#Values
sigma_sig = sigma_sm + 2.*alpha*sigma_int + (alpha**2)*sigma_np

#Errors
e_sig = np.sqrt( e_sm**2 + 4.*(alpha**2)*(e_int**2) + (alpha**4)*(e_np**2) )

##################################
## Calculate minimum luminosity ##
##################################

#Values
l1 = nEvents/sigma_sig
l2 = ((nEvents**2)*sigma_sig)/((sigma_sig - sigma_sm)**2)

L_min = np.array([l1,l2]).max(axis=0) #choose maximum of l1,l2 for each pairing

#Error
e1 = (nEvents*e_sig)/(sigma_sig**2)

e_in = np.sqrt( 4.*(alpha**2)*(e_int**2) + (alpha**4)*(e_np**2) )
e_v = 2.*(sigma_sig - sigma_sm)*e_in
v = (sigma_sig - sigma_sm)**2
e2 = ((nEvents*nEvents*sigma_sig)/v)*np.sqrt( (e_sig/sigma_sig)**2 + (e_v/v)**2 ) 

e_L_min = np.empty( len(alpha), dtype=object )
for i in range(0, len(e_L_min)):
    if L_min[i] == l1[i]:
        e_L_min[i] = e1[i]
    if L_min[i]== l2[i]:
        e_L_min[i] = e2[i]

#Print results
for j in range(0, len(alpha)):
    print "alpha = ",alpha[j],": minLum = ",L_min[j]," +- ",e_L_min[j]

##################################################
## plot max of l1 and l2, this is the minimum L ##
##################################################
#plt.scatter(alpha, L_min)
#plt.yscale("log")
#plt.show()
