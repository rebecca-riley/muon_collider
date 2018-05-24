import matplotlib.pyplot as plt
import cuts
from progressbar import AdaptiveETA, Bar, Percentage, ProgressBar, SimpleProgress


num_bins = 150


def main():
    file_data = fileReadIn()
    processSelection(plotReadIn(),file_data)
    return

def fileReadIn():
    file_input = input('Enter event files to plot: ').split()   #event files must be
                                                    #entered by their full path name
    if 'quit' in file_input:            #quit if user wants to exit
        quit()

    file_read = []                      #tries to read each file; allows user to try
    file_data = []                         #again if name is incorrect
    for file in file_input:
        try:
            f = open(file,'r')
            file_read.append(f)
        except IOError:
            print(file + ' not found. Try again with corrected input.')
            return fileReadIn()

    for file in file_read:              #read in events from each file
        print('Processing ' + file.name + '...')
        file_data.append(cuts.processEvents(file))

    if len(file_data) == 0:                #report number of events read
        print('No events read')
        return
    else:
        total_events = 0
        for event in file_data:
            total_events += len(event)
        print(str(total_events) + ' events read.')    

    return file_data

def plotReadIn():
    plots = input('Enter desired plots. Type \'help\' for options or \'quit\' to ' +
                  'exit. ').split()

    while len(plots) == 0:
        plots = input('No plots specified. Enter the tags for the desired plots. Type'
                      ' \'help\' for options. ').split()

    if 'quit' in plots:
        quit()

    if 'help' in plots:
        print('[Options]')
        print('final total invariant mass: massfin')
        print('final partial invariant_mass: massfinpar')
        print('initial total invariant mass: massinit')
        print('initial partial invariant_mass: massinitpar')
        print('final angle between particles: aglfin')
        print('initial angle between particles: aglinit')
        return plotReadIn()

    return plots

def processSelection(plots,file_data):
    for option in plots:
        if option not in {'massfin','massinit','massfinpar','massinitpar','aglfin','aglinit'}:
            print('The plot option you specified could not be found.')
            processSelection(plotReadIn(),file_data)

    if 'massfin' in plots:
        plotFinalInvariantMass(file_data)
    if 'massinit' in plots:
        plotInitialInvariantMass(file_data)
    if 'massfinpar' in plots:
        particle_list = input('Enter particle codes for partial invariant mass: ').split()
        plotFinalInvariantMass(file_data, particle_list)
    if 'massinitpar' in plots:
        particle_list = input('Enter particle codes for partial invariant mass: ').split()
        plotInitialInvariantMass(file_data, particle_list)
    if 'aglfin' in plots:
        particle_list = input('Enter two particle codes for angle between: ').split()
        plotFinalAngle(file_data, particle_list)
    if 'aglinit' in plots:
        particle_list = input('Enter two particle codes for angle between: ').split()
        plotInitialAngle(file_data, particle_list)


def plotFinalInvariantMass(file_data,particle_list=[]):
    plot(getDataToPlot(file_data,cuts.getInvariantMass,cuts.final_state,particle_list),'Final invariant mass histogram','Invariant mass')

def plotInitialInvariantMass(file_data,particle_list=[]):
    plot(getDataToPlot(file_data,cuts.getInvariantMass,cuts.initial_state,particle_list),'Initial invariant mass histogram','Invariant mass')

def plotFinalAngle(file_data,particle_list):
    plot(getDataToPlot(file_data,cuts.getAngle,cuts.final_state,particle_list),'Histogram of angle between '+particle_list[0]+' and '+particle_list[1],'Angle')

def plotInitialAngle(file_data,particle_list):
    plot(getDataToPlot(file_data,cuts.getAngle,cuts.initial_state,particle_list),'Histogram of angle between '+particle_list[0]+' and '+particle_list[1],'Angle')

def getDataToPlot(file_data,fctn,state,particle_list):
    data_to_plot = []
    for file_events in file_data:
        data_to_plot.append(extractEvent(file_events,fctn,state,particle_list))
    return data_to_plot

def extractEvent(file_data,fctn,state,particle_list):
    _event = []
    temp = []

    pbar = ProgressBar(widgets=['(', SimpleProgress(),') ', Percentage(),' ', Bar(),' ', AdaptiveETA()],maxval=len(file_data)).start()

    for event in pbar(file_data):
        event_data = cuts.getEventData(event)  #retrieve relevant data
        if fctn == cuts.getAngle:
            temp.append(fctn(event_data,state,particle_list[0],particle_list[1]))
        else:
            temp.append(fctn(event_data,state,particle_list))
    _event.append(temp)
    return _event

def plot(data,title,x_label):
    colors = ['b','g','r','o','y']

    for i in range(len(data)):
        plt.hist(data[i], num_bins, facecolor=colors[i], alpha = 0.5)      

    plt.xlabel(x_label)
    plt.ylabel('Num events')
    plt.title(title)
    # plt.autoscale(tight=True)
    # plt.axis([0, 15000, 0, 12500])
    plt.grid(True)
    plt.show()


if __name__ == '__main__':
    main()
