import cuts
import get_cross_section

# open input/output files
# filename = input('Enter event file for modified cross section: ').strip()
filenames = ['ee_z_low_500.lhe','ee_sm_250.lhe','ee_sm_500.lhe','ee_small_250.lhe',
             'ee_low_250.lhe','ee_low_500.lhe','ee_xa_sm_250.lhe','ee_xa_low_250.lhe',
             'mu_a_low_6500.lhe','mu_h_low_6500.lhe','mu_sm_1000.lhe','mu_sm_10000.lhe',
             'mu_low_6500.lhe','mu_z_low_6500.lhe','mu_sm_500.lhe','mu_low_500.lhe',
             'mu_xa_sm_250.lhe']
cut_file = open('nothing.txt','w')   #write only mode for output

# if filename == 'quit':              #quit if user wants to exit
#     quit()

event_file = 0
initial_cross_section = 0

for filename in filenames:
    try:                                #try to open file with inputted filename
        event_file = open(filename,'r')
        print(filename.upper())
        initial_cross_section = float(get_cross_section.getCrossSection(event_file))
        print('Initial cross section: ' + str(initial_cross_section))
    except IOError:                     #give error message, exit if file not found
        print(filename + ' not found. Try again with corrected input.')
        quit()

    event_list = cuts.processEvents(event_file,cut_file) #extract events from input file
    total_events = len(event_list)
    print('Number of events read: ' + str(total_events))

    fails_cut = [0, 0, 0]
    for event in event_list:      #determine for each event if it passes cuts
        fails_cut[cuts.passesCuts(event,True)] += 1

    number_remaining = len(event_list) - fails_cut[1]
    percent_passing = number_remaining/total_events
    print('Percent of events passing first cut: ' + str(percent_passing*100))
    print('Modified cross section: ' + str(initial_cross_section*percent_passing))
    number_remaining = number_remaining - fails_cut[2]
    percent_passing = number_remaining/total_events
    print('Percent of events passing both cuts: ' + str(percent_passing*100))
    print('Modified cross section: ' + str(initial_cross_section*percent_passing))

    event_file.close()              #close open files
