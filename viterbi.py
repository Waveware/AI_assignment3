
# 2D Robot Localization for AI Assignment 3
# by A1767895

import argparse

class Context:
    def __init__(self) -> None:
        self.map_dimensions = None
        self.map = []
        self.obs = []
        self.error_rate = 0.0
    
    def parse(self, input):
        sensor_observations = 0; row = 0; observations_count = 0
        state = ('DIMENSIONS')
        for line in input:
            if (state == 'DIMENSIONS'):
                self.map_dimensions = line.split(' ')
                state = 'MAP'
                continue

            if (state == 'MAP'):
                if (row < int(self.map_dimensions[0])):
                    self.map.append(line.split(' '))
                    row += 1
                else:
                    state = 'SENSOR'
            
            if (state == 'SENSOR'):
                sensor_observations = int(line)
                state = 'OBSERVATIONS'
                continue

            if (state == 'OBSERVATIONS'):
                if observations_count < sensor_observations:
                    self.obs.append(list(line))
                    observations_count += 1
                else:
                    state = 'ERROR_RATE'
            
            if (state == 'ERROR_RATE'):
                self.error_rate = float(line)

    def print(self) -> None:
        print('Dimensions: ' + str(self.map_dimensions))
        for row in self.map:
            print(row)
        print('Sensor Observations Count: NSWE' + str(len(self.obs)))
        for observe in self.obs:
            print(observe)
        print('Error rate: '+ str(self.error_rate))



def main():
##### Take input
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type=argparse.FileType('r'))
    args = parser.parse_args()
    raw = args.filename.read()
    input = raw.split('\n')
    m = Context()
    m.parse(input)
    m.print()
##### Take Input 

# Initialise empty Trellis matrix of expected size


if __name__ == "__main__":
    main()