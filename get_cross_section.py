# list of files to get cross section for
filenames = ['ee_high_250.lhe','ee_low_500.lhe']

for file in filenames:
    try:                                #try to open file with inputted filename
        event_file = open(file,'r')
        for line in event_file:
            if 'Integrated weight (pb) ' in line:
                print(file + line)
                break
        event_file.close()
    except IOError:                     #give error message, exit if file not found
        print(file + ' not found. Check list in script.')
        
