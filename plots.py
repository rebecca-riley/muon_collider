#### IMPORT DECLARATIONS ####
import matplotlib.pyplot as plt
import numpy as np
import cuts
import tabCompleter
from progressbar import AdaptiveETA, Bar, Percentage, ProgressBar, SimpleProgress


#### VARIABLE DEFINITIONS ####
num_bins = 150
percentile_to_show_x = 98
padding_multiplier_over_top_y = 1.1
transparency = 0.5


#### FUNCTION DEFINITIONS ####

#--- IO functions ---#

# returns list of event lists, one event list per specified file
def fileReadIn():
    tabCompleter.tabCompleter()         # configure tab completer
    file_input = input('Enter event files to plot: ').split()   #event files must be
                                                    #entered by their full path name
    if 'quit' in file_input:            #quit if user wants to exit
        quit()

    file_read = []                      #list of opened file pointers
    file_data = []                      #list of event lists, one event list per file
    for file in file_input:             #tries to read each file; allows user to try
        try:                            #again if name is incorrect
            f = open(file,'r')
            file_read.append(f)
        except IOError:
            print(file + ' not found. Try again with corrected input.')
            return fileReadIn()

    for file in file_read:              #for each file, adds event list to file_data
        print('Processing ' + file.name + '...')
        file_data.append(cuts.processEvents(file))

    if len(file_data[0]) == 0:          #if no events read, quit script
        print('No events read')
        quit()
    else:                               #else report total number of events read
        total_events = 0
        for event in file_data:
            total_events += len(event)
        print(str(total_events) + ' events read.')    

    return file_data                    #returns list of event lists

# returns list of user-desired plotting options
def plotReadIn():
    plots = input('Enter desired plots. Type \'help\' for options or \'quit\' to ' +
                  'exit. ').split()

    while len(plots) == 0:              #if no input entered, prompt until it is
        plots = input('No plots specified. Enter the tags for the desired plots. Type'
                      ' \'help\' for options. ').split()

    if 'quit' in plots:                 #quit if 'quit' appears anywhere in input
        quit()

    if 'help' in plots:                 #report options if 'help' anywhere in input
        print('[Options]')
        print('final total invariant mass: massfin')
        print('final partial invariant_mass: massfinpar')
        print('initial total invariant mass: massinit')
        print('initial partial invariant_mass: massinitpar')
        print('final angle between particles: aglfin')
        print('initial angle between particles: aglinit')
        print('final photon energy: ptnenfin')
        print('initial photon energy: ptneninit')
        print('final z energy: zenfin')
        return plotReadIn()             #prompt for input again

    return plots                        #return list of desired plotting options

# parses user-inputted options and calls associated plotting functions
def processSelection(plots,file_data):
    for option in plots:        #if any option is not recognized, reprompt for input
        if option not in {'massfin','massinit','massfinpar','massinitpar','aglfin',\
                          'aglinit','ptnenfin','ptneninit','zenfin','all'}:
            print('The plot option you specified could not be found.')
            processSelection(plotReadIn(),file_data)
            return

    #change default percentile to show from 98 to 100
    if 'all' in plots:
        global percentile_to_show_x
        percentile_to_show_x = 100
    #for each specified plot option, process data for and output that plot
    if 'ptnenfin' in plots or 'ptneninit' in plots:
        which_photon = 0
        which_photon_input = input('Enter which photon. No value entered defaults '\
                                   'to zero: ').strip()
        if len(which_photon_input) == 0:
            pass
        else:
            try:
                int(which_photon_input)
            except ValueError:
                print('Value entered must be an integer. Enter plot options again.')
                processSelection(plots,file_data)
                return

        if 'ptnenfin' in plots:
            plotFinalPhotonEnergy(file_data,which_photon)
        if 'ptneninit' in plots:
            plotInitialPhotonEnergy(file_data,which_photon)
    if 'zenfin' in plots:
        plotFinalZEnergy(file_data,0)
    if 'massfin' in plots:
        plotFinalInvariantMass(file_data)
    if 'massinit' in plots:
        plotInitialInvariantMass(file_data) #@later make prtcl code input more robust
    if 'massfinpar' in plots:           #require particle codes for partial inv. mass
        particle_list = input('Enter particle codes for partial invariant mass: ').split()
        plotFinalInvariantMass(file_data, particle_list)
    if 'massinitpar' in plots:
        particle_list = input('Enter particle codes for partial invariant mass: ').split()
        plotInitialInvariantMass(file_data, particle_list)
    if 'aglfin' in plots:               #require 2 particle codes for angle between
        particle_list = input('Enter two particle codes for angle between: ').split()
        plotFinalAngle(file_data, particle_list)
    if 'aglinit' in plots:
        particle_list = input('Enter two particle codes for angle between: ').split()
        plotInitialAngle(file_data, particle_list)


#--- plotting functions ---#

# calls plot function with parameters for plotting final, invariant mass (total or
# partial)
def plotFinalInvariantMass(file_data,particle_list=[]):
    plot(getDataToPlot(file_data,cuts.getInvariantMass,cuts.final_state,particle_list),\
         'Final invariant mass histogram','Invariant mass')

# calls plot function with parameters for plotting initial, invariant mass (total or
# partial)
def plotInitialInvariantMass(file_data,particle_list=[]):
    plot(getDataToPlot(file_data,cuts.getInvariantMass,cuts.initial_state,particle_list),\
         'Initial invariant mass histogram','Invariant mass')

# calls plot function with parameters for plotting final angle between two particles
def plotFinalAngle(file_data,particle_list):
    plot(getDataToPlot(file_data,cuts.getAngle,cuts.final_state,particle_list),\
         'Histogram of angle between '+particle_list[0]+' and '+particle_list[1],'Angle')
    #@later find a way to accept input as label rather than using numbers

# calls plot function with parameters for plotting initial angle between two particles
def plotInitialAngle(file_data,particle_list):
    plot(getDataToPlot(file_data,cuts.getAngle,cuts.initial_state,particle_list),\
         'Histogram of angle between '+particle_list[0]+' and '+particle_list[1],'Angle')

# calls plot function with parameters for plotting final, single photon energy
def plotFinalPhotonEnergy(file_data,which_photon):
    plot(getDataToPlot(file_data,cuts.getPhotonEnergy,cuts.final_state,which_photon),\
         'Photon energy histogram','Energy')

# calls plot function with parameters for plotting initial, single photon energy
def plotInitialPhotonEnergy(file_data,which_photon):
    plot(getDataToPlot(file_data,cuts.getPhotonEnergy,cuts.initial_state,which_photon),\
         'Photon energy histogram','Energy')

# calls plot function with parameters for plotting final, single photon energy
def plotFinalZEnergy(file_data,which_z):
    plot(getDataToPlot(file_data,cuts.getZEnergy,cuts.final_state,which_z),\
         'Z energy histogram','Energy')

# return list of data points from each specified file in format acceptable for plotting
def getDataToPlot(file_data,fctn,state,particle_list):
    data_to_plot = []                   #each file_event is a list of events
    for file_events in file_data:       #associated with an input file
        data_to_plot.append(extractEvent(file_events,fctn,state,particle_list))
    return data_to_plot     #get data list for each file; return list of data lists

# returns list of desired data points extracted from event list of single file
def extractEvent(file_events,fctn,state,particle_list):
    data = []                           #array to hold desired data parsed from events

    #progress bar to show event processing progress
    pbar = ProgressBar(widgets=['(', SimpleProgress(),') ', Percentage(),' ', Bar(),\
           ' ', AdaptiveETA()],maxval=len(file_events)).start()

    for event in pbar(file_events):     #for each event in a file
        event_data = cuts.getEventData(event)   #fetch data from event in usable form
        if fctn == cuts.getAngle:       #use only first two particles for angle plots
            data.append(fctn(event_data,state,particle_list[0],particle_list[1]))
        else:                           #all other plots simply call fctn to extract
            data.append(fctn(event_data,state,particle_list))   #desired quantity
    return data                         #return list of desired data from one file

# outputs one plot for every plot option specified by the user; plots the data from
# each specified file on a single plot
def plot(data,title,x_label):
    colors = ['b','g','r','y','c','m','k']  #color sequence; each file's data gets a
                                            #different color on histogram
    plt.figure(id(data))                #associate each figure with a unique ID to
                                        #allow for multiple windows
    max_bin, max_range = 0,0
    for i in range(len(data)):          #for each file, plot extracted data as histo
        heights,bins,patches = plt.hist(data[i], num_bins, facecolor=colors[i], 
                                        alpha = transparency)      
        if max(heights) > max_bin:      #keep track of tallest bin
            max_bin = max(heights)

        if len(data[i]) > len(data[max_range]): #keep track of widest-ranging data
            max_range = i

    plt.xlabel(x_label)                 #set labels, title
    plt.ylabel('Number of events')
    plt.title(title)
    plt.axis([0,np.percentile(data[max_range],percentile_to_show_x),0, #x scale shows
              max_bin*padding_multiplier_over_top_y])       #percntl % of widest-ran-
    plt.grid(True)                                          #ging data; y is greater
                                                            #than tallest bin by the
                                                            #padding multiplier

#### EXECUTION SUBROUTINE ####

def main():
    file_data = fileReadIn()            #read in input files
    processSelection(plotReadIn(),file_data)    #read in and process plot options
    plt.show()                          #output plots
    return

if __name__ == '__main__':
    main()
