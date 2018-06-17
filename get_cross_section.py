def getCrossSection(event_file):
    for line in event_file:
        if 'Integrated weight' in line:
            return line.split()[5]

def main():
    # list of files to get cross section for
    files = open('files.txt','r')
    print('All cross sections given in picobarns.')

    for line in files:
        line = line.strip()
        try:                                #try to open file with inputted filename
            event_file = open(line,'r')
            print(line + ': ' + str(getCrossSection(event_file)))
            event_file.close()
        except IOError:                     #give error message, exit if file not found
            print(line + ' not found. Check list in script.')

if __name__ == '__main__':
    main()
