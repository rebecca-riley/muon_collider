import cuts
import get_cross_section

# open input/output files
filenames = open('files.txt','r')
out_file = open('out.txt','w')

# provide output format for out.txt
out_file.write('OUTPUT FORMAT' + '\n')
out_file.write('[FILENAME]' + '\n')
out_file.write('[initial cross section]' + '\n')
out_file.write('[percent of events passing first cut -- 1 = 1%, not 100%]' + '\n')
out_file.write('[new cross section]' + '\n')
out_file.write('[percent of events passing both cuts]' + '\n')
out_file.write('[final cross section]' + '\n\n')

# process cuts from each file
for line in filenames:
    filename = line.strip()             #remove newline character from filename
    try:                                #try to open file with inputted filename
        event_file = open(filename,'r')

        print(filename.upper())         #some details to terminal, all info to out.txt
        out_file.write(filename.upper() + '\n')
        
        initial_cross_section = float(get_cross_section.getCrossSection(event_file))
        out_file.write(str(initial_cross_section) + '\n')   #some info to terminal
                                                    #shows processing has started
        event_list = cuts.processEvents(event_file) #extract events from input file
        total_events = len(event_list)

        fails_cut = [0, 0, 0]
        for event in event_list:      #determine for each event if it passes cuts
            fails_cut[cuts.passesCuts(event,True)] += 1     #index codes for which
                                                            #cut event failed on
        number_remaining = len(event_list) - fails_cut[1]   #percent passing/cross
        percent_passing = number_remaining/total_events     #section after first cut
        out_file.write(str(percent_passing*100) + '\n')
        out_file.write(str(initial_cross_section*percent_passing) + '\n')
        
        number_remaining = number_remaining - fails_cut[2]  #percent passing/cross
        percent_passing = number_remaining/total_events     #section after second cut
        print('Percent of events passing both cuts: ' + str(percent_passing*100))
        out_file.write(str(percent_passing*100) + '\n')
        print('Final modified cross section: ' + str(initial_cross_section*percent_passing))
        out_file.write(str(initial_cross_section*percent_passing) + '\n')

        event_file.close()

    except IOError:                     #quit with error message if file not found
        print(filename + ' not found. Try again with corrected input.')
        quit()

print('Details written to out.txt.')
