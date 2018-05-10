# VARIABLE DEFINITIONS
file_in = 'composite_100k.lhe'
file_out = 'composite_cut.lhe'

# FUNCTION DEFINITIONS
# writes events that we want to keep to the file
def processEvent(cut_file):
    cut_file.write(event)       #writes all events back out with no processing

# EXECUTION SUBROUTINE
# open input/output files
event_file = open(file_in,'r')  #read only mode for input
cut_file = open(file_out,'w')   #write only mode for output

in_event = False                #flag to indicate whether in event block
event = ''                      #string to store event block data

# line processing loop
for line in event_file:
    if line == '<event>\n':     #search file for start of event block
        in_event = True
    if in_event == False:       #if not in event block, write line back out
        cut_file.write(line)    #to file
    if in_event == True:        #if in event, collect info in event string
        event += line
    if line == '</event>\n':    #once event ends, process the data in the event,
        in_event = False        #reset the in_event flag, and clear storage str
        processEvent(cut_file)
        event = ''

event_file.close()              #close open files
cut_file.close()
