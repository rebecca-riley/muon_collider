import matplotlib.pyplot as plt
import cuts

num_bins = 150

def main():
    file_input = input('Enter event files to plot: ').split()

    file_read = []
    events = []
    for file in file_input:
        try:
            f = open(file,'r')
            file_read.append(f)
            events.append(cuts.processEvents(f))
        except IOError:
            print(file + ' not found. Try again with corrected input.')
            return

    if len(events) == 0:
        print('No events read')
        return 
    print(len(events[0]))

    plots = input('Enter desired plots. Type \'help\' for options. ').split()

    while len(plots) == 0:
        plots = input('No plots specified. Enter the tags for the desired plots. Type'
                      ' \'help\' for options. ').split()

    if plots[0] == 'help':
        print('[Options]')
        print('final total invariant mass: massfin')
        print('final partial invariant_mass: massfinpar')
        print('initial total invariant mass: massinit')
        print('initial partial invariant_mass: massinitpar')
        print('final angle between particles: aglfin')
        print('initial angle between particles: aglinit')
        plots = input('Enter parameter to plot: ').split()

    # num_bins = int(input('Number of bins? '))

    if 'massfin' in plots:
        plotFinalInvariantMass(events)
    if 'massinit' in plots:
        plotInitialInvariantMass(events)
    if 'massfinpar' in plots:
        particle_list = input('Enter particle codes for partial invariant mass: ').split()
        plotFinalInvariantMass(events, particle_list)
    if 'massinitpar' in plots:
        particle_list = input('Enter particle codes for partial invariant mass: ').split()
        plotInitialInvariantMass(events, particle_list)
    if 'aglfin' in plots:
        particle_list = input('Enter two particle codes for angle between: ').split()
        plotFinalAngle(events, particle_list)
    if 'aglinit' in plots:
        particle_list = input('Enter two particle codes for angle between: ').split()
        plotInitialAngle(events, particle_list)

    return


def plotFinalInvariantMass(events,particle_list=[]):
    plot(extractInvariantMass(events,'1',particle_list),'Final invariant mass histogram','Invariant mass')

def plotInitialInvariantMass(events,particle_list=[]):
    plot(extractInvariantMass(events,'-1',particle_list),'Initial invariant mass histogram','Invariant mass')

def plotFinalAngle(events,particle_list):
    plot(extractAngle(events,'1',particle_list),'Histogram of angle between '+particle_list[0]+' and '+particle_list[1],'Angle')

def plotInitialAngle(events,particle_list):
    plot(extractAngle(events,'-1',particle_list),'Histogram of angle between '+particle_list[0]+' and '+particle_list[1],'Angle')

def extractInvariantMass(events,state,particle_list=[]):
    return extractEvent(cuts.getInvariantMass,events,state,particle_list)

def extractAngle(events,state,particle_list):
    return extractEvent(cuts.getAngle,events,state,particle_list)

def extractEvent(fctn,events,state,particle_list):
    _event = []
    for i in range(len(events)):
        temp = []
        for event in events[i]:
            if fctn == cuts.getAngle:
                temp.append(fctn(event,state,particle_list[0],particle_list[1]))
            else:
                temp.append(fctn(event,state,particle_list))
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

