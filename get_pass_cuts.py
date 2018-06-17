import cuts
import get_cross_section

# open input/output files
# filename = input('Enter event file for modified cross section: ').strip()
filenames = open('files.txt','r')
cut_file = open('nothing.txt','w')   #write only mode for output
out_file = open('out.txt','w')

# if filename == 'quit':              #quit if user wants to exit
#     quit()

event_file = 0
initial_cross_section = 0

for line in filenames:
    filename = line.strip()
    try:                                #try to open file with inputted filename
        event_file = open(filename,'r')
        print(filename.upper())
        out_file.write(filename.upper() + '\n')
        initial_cross_section = float(get_cross_section.getCrossSection(event_file))
        out_file.write(str(initial_cross_section) + '\n')
    except IOError:                     #give error message, exit if file not found
        print(filename + ' not found. Try again with corrected input.')
        quit()

    event_list = cuts.processEvents(event_file,cut_file) #extract events from input file
    total_events = len(event_list)

    fails_cut = [0, 0, 0]
    for event in event_list:      #determine for each event if it passes cuts
        fails_cut[cuts.passesCuts(event,True)] += 1

    number_remaining = len(event_list) - fails_cut[1]
    percent_passing = number_remaining/total_events
    out_file.write(str(percent_passing*100) + '\n')
    out_file.write(str(initial_cross_section*percent_passing) + '\n')
    number_remaining = number_remaining - fails_cut[2]
    percent_passing = number_remaining/total_events
    print('Percent of events passing both cuts: ' + str(percent_passing*100))
    out_file.write(str(percent_passing*100) + '\n')
    print('Final modified cross section: ' + str(initial_cross_section*percent_passing))
    out_file.write(str(initial_cross_section*percent_passing) + '\n')

    event_file.close()              #close open files

print('Details written to out.txt.')
