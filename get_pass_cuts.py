import cuts

# open input/output files
filename = input('Enter event file for modified cross section: ').strip()
cut_file = open('nothing.txt','w')   #write only mode for output

if filename == 'quit':              #quit if user wants to exit
    quit()

try:                                #try to open file with inputted filename
    event_file = open(filename,'r')
except IOError:                     #give error message, exit if file not found
    print(filename + ' not found. Try again with corrected input.')
    quit()

event_list = cuts.processEvents(event_file,cut_file) #extract events from input file

print('Number of events read: ' + str(len(event_list)))

fails_cut = [0, 0, 0]
for event in cuts.pbar(event_list):      #determine for each event if it passes cuts
    fails_cut[cuts.passesCuts(event,True)] += 1

print(fails_cut[0])
print(fails_cut[1])
print(fails_cut[2])

event_file.close()              #close open files
