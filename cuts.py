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

#### FUNCTION DEFINITIONS ####
#--- cut functions ---#
#calculates invariant mass for each event
def getInvariantMass(event_data):
    x_p = extractEventData(event_data,x_index)
    y_p = extractEventData(event_data,y_index)
    z_p = extractEventData(event_data,z_index)
    energy = extractEventData(event_data,energy_index)

    return sum(energy)**2 - sum(x_p)**2 - sum(y_p)**2 - sum(z_p)**2

#--- processing functions ---#
# writes events that we want to keep to the file
def processEvent(cut_file,event):
    event_block = event.splitlines()    #store event line by line
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
