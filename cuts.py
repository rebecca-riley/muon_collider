# VARIABLE DEFINITIONS
file_in = 'a.lhe'
file_out = 'a_cut.lhe'

# magic number constants for event processing
line_results_start = 4
num_results = 3
mass_index = 10
mass_precision = 10

# FUNCTION DEFINITIONS
# writes events that we want to keep to the file
def processEvent(cut_file):
    data = event.splitlines()   #store event line by line
    data = data[line_results_start:]  #throw away irrelevant beginning lines

    mass_total = 0              #test writes mass total to output file
    test = ['','','']
    mass = ['','','']

    for i in range(num_results):    #for each collision product
        test[i] = data[i].split()   #isolate each column
        mass[i] = test[i][mass_index]       #pick out mass term
        mass[i] = mass[i][0:mass_precision]    #truncate end of mass term
        mass_total += float(mass[i])   #typecast mass to float, incr total

    cut_file.write(str(mass_total)+"\n")    #write mass out, not whole event

#cut_file.write(event)          #writes all events back out with no processing


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
