#### IMPORT DECLARATIONS ####
from vector import Vector
import math
from progressbar import ProgressBar
pbar = ProgressBar()


#### VARIABLE DEFINITIONS ####

# magic number constants for event processing
particle_identity_index = 0
initial_final_index = 1
x_index, y_index, z_index, energy_index = 6, 7, 8, 9
mass_index = 10
spin_index = 12

null_particle = '0'
photon = '22'
mu_minus, mu_plus = '13', '-13'
tau_minus, tau_plus = '15', '-15'
z = '23'
higgs = '25'

initial_state = '-1'
mid_state = '2'
final_state = '1'


#### FUNCTION DEFINITIONS ####

#--- cut functions ---#

# boolean function indicating whether event passes or fails cuts
def passesCuts(event):
    event_data = getEventData(event)  #retrieve relevant data

    # mass cut on two final taus
    inv_mass_tt = getInvariantMass(event_data,final_state,[tau_plus,tau_minus])
    if inv_mass_tt > 80 and inv_mass_tt < 100:
        return False

    # mass cut on final taus and photon
    inv_mass_tta = getInvariantMass(event_data,final_state,[tau_plus,tau_minus,photon])
    if inv_mass_tta > 130 or inv_mass_tta < 120:
        return False

    return True


#--- get functions ---#

# returns invariant mass for specified state of a single event
# optional: if you want to get the invariant mass for specific particles, you can pass
#           in a list with their particle codes; default will return the invariant
#           mass for all particles in given state
def getInvariantMass(event_data,event_state,particle_list=[]):
    indices, sum_vec = [x_index,y_index,z_index,energy_index], [0,0,0,0]

    for i in range(len(indices)):   #for each 4p index, extract & sum all final values
        if particle_list == []:
            sum_vec[i] = sum(_extractEventSubset(event_data,indices[i],event_state,
                             null_particle))
        else:
            for particle in particle_list:
                sum_vec[i] += sum(_extractEventSubset(event_data,indices[i],
                                  event_state,particle))

    # return invariant mass: E^2 - x^2 - y^2 - z^2
    return math.sqrt(sum_vec[3]**2 - sum_vec[0]**2 - sum_vec[1]**2 - sum_vec[2]**2)


# returns the angle in degrees between two specified particles in a given state
# optional: if you have more than one particle in a given state (e.g. your process
#           creates two photons), you can specify which of the two photons you want
#           to consider with the which_particle parameter; default value is the first
#           particle found
# raises:   ValueError if no events found matching input parameters
#           IndexError if requested which_particle index does not exist (this might
#           occur if there are less particles in the given state than the requested
#           index)
def getAngle(event_data,event_state,particle1_code, particle2_code,which_particle1=0,
             which_particle2=0):
    p1, p2 = [], []

    for index in [x_index,y_index,z_index]:
        subset1 = _extractEventSubset(event_data,index,event_state,particle1_code)
        subset2 = _extractEventSubset(event_data,index,event_state,particle2_code)
        if len(subset1) == 0 or len(subset2) == 0:
            raise ValueError('no events found matching the given particle/state')
        if which_particle1 >= len(subset1) or which_particle2 >= len(subset2):
            raise IndexError('particle instance index out of range')
        p1.append(subset1[which_particle1])
        p2.append(subset2[which_particle2])

    vec1 = Vector(p1[0],p1[1],p1[2])
    vec2 = Vector(p2[0],p2[1],p2[2])

    return math.degrees(math.acos(vec1.inner(vec2)/(vec1.norm()*vec2.norm())))


# returns the energy of a specified particle in a given state
# optional: if you have more than one particle in a given state, you can specify which
#           one you want to consider with the which_particle parameter; default value
#           is the first particle found
# raises:   ValueError if no events found matching input parameters
#           IndexError if requested which_particle index does not exist (this might
#           occur if there are less photons in the given state than the requested
#           index)
def getEnergy(event_data,event_state,particle_label,which_particle=0):
    energy = _extractEventSubset(event_data,energy_index,event_state,particle_label)
    if len(energy) == 0:
        raise ValueError('no particles found in the given state')
    if which_particle >= len(energy):
        raise IndexError('particle instance index out of range')
    return energy[which_particle]

# returns the energy of a photon for backwards compatibility
def getPhotonEnergy(event_data,event_state,which_particle=0):
    return getEnergy(event_data,event_state,photon,which_particle)

# returns the energy of the z for backwards compatibility
def getZEnergy(event_data,event_state,which_particle=0):
    return getEnergy(event_data,event_state,z,which_particle)


#--- deprecated ---#
# alternate function to return the energy of a specified photon in a given state
# note:     _detPhotonEnergy is less efficient than getPhotonEnergy, so getPhotonEnergy
#           will be used by default
# optional: if you have more than one photon in a given state, you can specify which
#           one you want to consider with the which_particle parameter; default value
#           is the first particle found
# raises:   ValueError if no events found matching input parameters
#           IndexError if requested which_particle index does not exist (this might
#           occur if there are less photons in the given state than the requested
#           index)
def _getPhotonEnergyAlternate(event_data,event_state,which_particle=0):
    p = []

    for index in [x_index,y_index,z_index]:
        subset = _extractEventSubset(event_data,index,event_state,photon)
        if len(subset) == 0:
            raise ValueError('no photons found in the given state')
        if which_particle >= len(subset):
            raise IndexError('photon instance index out of range')
        p.append(subset[which_particle])

    # E_photon = norm(p_photon)
    return math.sqrt(p[0]**2 + p[1]**2 + p[2]**2)


#--- extraction functions ---#

# returns list of rows (strings) containing collision data
# event block is the entire block of event text, from <event> to <\event>
# event data is the rows in the event block containing collision data
def getEventData(event):
    event_block = event.splitlines()        #store event line by line
    i = 1                       #data[0] = <event>; data[1] = event info
    while(i<len(event_block)):  #search for line starting in '<' (end of event block)
        if event_block[i][0] == '<':
            break               #@later more elegant way to do this?
        else:
            i += 1
    
    return event_block[2:i]     #throw away irrelevant lines at beginning/end

# returns a list of numbers extracted from event data at given index
def extractEventData(event_data,index_to_extract):
    extraction = []
    for row in event_data:      #loops over each row in event data
        extraction.append(float(row.split()[index_to_extract]))  #conversion to float
    return extraction           #list of extraced numbers

# hidden function to return a list of data points for particles meeting identity,
# index, and state requirements
def _extractEventSubset(event_data,index_to_extract,event_state,particle_code):
    event_subset = []
    for row in event_data:
        element_list = row.split()
        if element_list[initial_final_index] == event_state:    #if in correct state
            #if no particle stated or particle match is correct
            if particle_code == null_particle or \
            element_list[particle_identity_index] == particle_code:
                event_subset.append(row)        #collect desired data
    return extractEventData(event_subset,index_to_extract)

# returns a list of data points associated with initial particles for a specified index
# optional: specify particle identity; if no particle specified, returns all initial
#           events
def extractInitialEvents(event_data,index_to_extract,particle_code=null_particle):
    return _extractEventSubset(event_data,index_to_extract,initial_state,particle_code)

# returns a list of data points associated with final particles for a specified index
# optional: specify particle identity; if no particle specified, returns all final
#           events
def extractFinalEvents(event_data,index_to_extract,particle_code=null_particle):
    return _extractEventSubset(event_data,index_to_extract,final_state,particle_code)

# returns a list of data points associated with intermediate particles for a specified index
# optional: specify particle identity; if no particle specified, returns all
#           intermediate events
def extractIntermediateEvents(event_data,index_to_extract,particle_code=null_particle):
    return _extractEventSubset(event_data,index_to_extract,mid_state,particle_code)


#--- processing functions ---#

# returns events from lhe file in a list of strings
def processEvents(event_file,cut_file=None):
    in_event = False                #flag to indicate whether in event block
    event = ''                      #string to store event block data
    event_list = []
    #contnu = True                  #DEBUG -- ALLOWS PROGRAM TO RUN OVER ONE EVENT ONLY

    # line processing loop
    for line in event_file:
    #    if contnu == True:             #DEBUG -- AFTER ONE EVENT, STOP EXECUTION
            if line == '<event>\n':     #search file for start of event block
                in_event = True
            if in_event == False and cut_file != None:  #if not in event block and
                cut_file.write(line)    #cut file provided, write line back out to file
            if in_event == True:        #if in event, collect info in event string
                event += line
            if line == '</event>\n':    #once event ends, process the data in the event,
                in_event = False        #reset the in_event flag, and clear storage str
                event_list.append(event)
                event = ''
    #            contnu = False         #DEBUG -- AFTER ONE EVENT, STOP EXECUTION

    return event_list


#### EXECUTION SUBROUTINE ####

def main():
    # open input/output files
    filename = input('Enter event file to cut on: ').strip()

    if filename == 'quit':              #quit if user wants to exit
        return

    try:                                #try to open file with inputted filename
        event_file = open(filename,'r')
    except IOError:                     #give error message, exit if file not found
        print(filename + ' not found. Try again with corrected input.')
        return

    filename_split = filename.split('.')    #create formulaic output filename (add _cut)
    filename_out = filename_split[0] + '_cut.' + '.'.join(filename_split[1:])
    
    cut_file = open(filename_out,'w')   #write only mode for output
    print('Writing cut events to ' + filename_out)  #let user know output filename

    event_list = processEvents(event_file,cut_file) #extract events from input file

    k=0                                 #counter to track # of events written out
    for event in pbar(event_list):      #determine for each event if it passes cuts
        if passesCuts(event):
            cut_file.write(event)       #write out full event meeting cut criteria
            k += 1                      #update number of events passing all cuts

    print(str(k) + ' events written to ' + filename_out)    #print number of events
                                                            #written out
    event_file.close()              #close open files
    cut_file.close()

if __name__ == '__main__':
    main()
