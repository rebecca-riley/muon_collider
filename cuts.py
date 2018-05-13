#### IMPORT DECLARATIONS ####
from vector import Vector
import math

#### VARIABLE DEFINITIONS ####
file_in = 'composite_100k.lhe'
file_out = 'composite_cut.lhe'

# magic number constants for event processing
particle_identity_index = 0
initial_final_index = 1
x_index = 6
y_index = 7
z_index = 8
energy_index = 9
mass_index = 10
spin_index = 11

null_particle = '0'
photon = '22'
mu_minus = '13'
mu_plus = '-13'
tau_minus = '15'
tau_plus = '-15'
higgs = '25'

initial_event = '-1'
mid_event = '2'
final_event = '1'

#### FUNCTION DEFINITIONS ####
#--- cut functions ---#
#calculates invariant mass for each event
def getInvariantMass(event_data):
    x_p = extractFinalEvents(event_data,x_index,photon)[0]
    y_p = extractFinalEvents(event_data,y_index,photon)[0]
    z_p = extractFinalEvents(event_data,z_index,photon)[0]
    energy = extractFinalEvents(event_data,energy_index,photon)[0]

    x_p += extractFinalEvents(event_data,x_index,mu_plus)[0]
    y_p += extractFinalEvents(event_data,y_index,mu_plus)[0]
    z_p += extractFinalEvents(event_data,z_index,mu_plus)[0]
    energy += extractFinalEvents(event_data,energy_index,mu_plus)[0]

    x_p += extractFinalEvents(event_data,x_index,mu_minus)[0]
    y_p += extractFinalEvents(event_data,y_index,mu_minus)[0]
    z_p += extractFinalEvents(event_data,z_index,mu_minus)[0]
    energy += extractFinalEvents(event_data,energy_index,mu_minus)[0]

    return math.sqrt(energy**2 - x_p**2 - y_p**2 - z_p**2)

def getAngle(event_data):
    px_photon = extractFinalEvents(event_data,x_index,photon)
    py_photon = extractFinalEvents(event_data,y_index,photon)
    pz_photon = extractFinalEvents(event_data,z_index,photon)

    px_mu_plus = extractFinalEvents(event_data,x_index,mu_plus)
    py_mu_plus = extractFinalEvents(event_data,y_index,mu_plus)
    pz_mu_plus = extractFinalEvents(event_data,z_index,mu_plus)


    # test to make sure lengths are the same
#    for i in range(len(px_photon)):
    vec_photon = Vector(px_photon[0],py_photon[0],pz_photon[0])
#    print(vec_photon)

#    for i in range(len(px_mu_plus)):
    vec_mu_plus = Vector(px_mu_plus[0],py_mu_plus[0],pz_mu_plus[0])
#    print(vec_mu_plus)

    return vec_mu_plus.inner(vec_photon)/(vec_mu_plus.norm()*vec_photon.norm())

#--- processing functions ---#
# writes events that we want to keep to the file
def processEvent(cut_file,event):
    event_block = event.splitlines()    #store event line by line
#    cut_file.write(str(getAngle(getEventData(event_block)))+'\n')
    cut_file.write(str(getInvariantMass(getEventData(event_block)))+'\n')
                                        #writes invariant mass to file

#    if mass_total>1 and mass_total<2:
#        cut_file.write(event)       #write out full event meeting cut criteria

# returns list of rows (strings) containing collision data
# event block is the entire block of event text, from <event> to <\event>
# event data is the rows in the event block containing collision data
def getEventData(event_block):
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
            if particle_code == null_particle or element_list[particle_identity_index] == particle_code:
                event_subset.append(row)        #collect desired data
    return extractEventData(event_subset,index_to_extract)

# returns a list of data points associated with initial particles for a specified index
# optional: specify particle identity; if no particle specified, returns all initial
#           events
def extractInitialEvents(event_data,index_to_extract,particle_code=null_particle):
    return _extractEventSubset(event_data,index_to_extract,initial_event,particle_code)

# returns a list of data points associated with final particles for a specified index
# optional: specify particle identity; if no particle specified, returns all final
#           events
def extractFinalEvents(event_data,index_to_extract,particle_code=null_particle):
    return _extractEventSubset(event_data,index_to_extract,final_event,particle_code)

# returns a list of data points associated with intermediate particles for a specified index
# optional: specify particle identity; if no particle specified, returns all
#           intermediate events
def extractIntermediateEvents(event_data,index_to_extract,particle_code=null_particle):
    return _extractEventSubset(event_data,index_to_extract,mid_event,particle_code)


#### EXECUTION SUBROUTINE ####
# open input/output files
event_file = open(file_in,'r')  #read only mode for input
cut_file = open(file_out,'w')   #write only mode for output

in_event = False                #flag to indicate whether in event block
event = ''                      #string to store event block data
#contnu = True                  #DEBUG -- ALLOWS PROGRAM TO RUN OVER ONE EVENT ONLY

# line processing loop
for line in event_file:
#    if contnu == True:             #DEBUG -- AFTER ONE EVENT, STOP EXECUTION
        if line == '<event>\n':     #search file for start of event block
            in_event = True
        if in_event == False:       #if not in event block, write line back out
            cut_file.write(line)    #to file
        if in_event == True:        #if in event, collect info in event string
            event += line
        if line == '</event>\n':    #once event ends, process the data in the event,
            in_event = False        #reset the in_event flag, and clear storage str
            processEvent(cut_file,event)
            event = ''
#            contnu = False         #DEBUG -- AFTER ONE EVENT, STOP EXECUTION

event_file.close()              #close open files
cut_file.close()
