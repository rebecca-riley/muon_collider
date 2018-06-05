# list of files to get cross section for
filenames = ['ee_z_low_500.lhe','ee_sm_250.lhe','ee_sm_500.lhe','ee_small_250.lhe',
             'ee_low_250.lhe','ee_low_500.lhe','ee_xa_sm_250.lhe','ee_xa_low_250.lhe',
             'mu_a_low_6500.lhe','mu_h_low_6500.lhe','mu_sm_1000.lhe','mu_sm_10000.lhe',
             'mu_low_6500.lhe','mu_z_low_6500.lhe','mu_sm_500.lhe','mu_low_500.lhe',
             'mu_xa_sm_250.lhe']

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

