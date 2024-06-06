
# 2D Robot Localization for AI Assignment 3
# by A1767895

import argparse
import numpy as np
from copy import deepcopy

def find_max(nested_list):
    m = -1.0
    r = 0; c = 0
    for row in nested_list:
        for col in row:
            if nested_list[r][c] > m:
                m = nested_list[r][c]
                position = [r, c]
            c += 1
        c = 0; r += 1
    return [m, position] 

def is_adjacent(x1, y1, x2, y2):
    x1 += 1; x2 += 1; y1 += 1; y2 += 1
    if x1 == x2 and y1 == y2:
        return 0
    if x1 == x2 and abs(y1-y2) == 1:
        return 1
    if y1 == y2 and abs(x1-x2) == 1:
        return 1
    return 0

class Context:
    def __init__(self) -> None:
        self.dim = None
        self.map = []
        self.obs = []   
        self.error_rate = 0.0
        self.t0 = []
        self.tm = []
        self.em = []
        self.K = 0 # Traversable points in map
    
    def parse(self, input):
        sensor_observations = 0; row = 0; col = 0; observations_count = 0
        state = ('DIMENSIONS')
        for line in input:
            if (state == 'DIMENSIONS'):
                self.dim = line.split(' ')
                state = 'MAP'
                continue

            if (state == 'MAP'):
                if (row < int(self.dim[0])):
                    c_row = line.split(' ')
                    while len(c_row) > int(self.dim[1]):
                        c_row.pop()
                    self.map.append(c_row)
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

    # returns a neighbour list for provided coordinates
    def neighbours(self, ns, we):
        nslen = int(self.dim[0])
        welen = int(self.dim[1])
        north = 0; south = 0; west = 0; east = 0

        if self.map[ns][we] == 'X':
            return [-1]
        
        # check north
        if ns > 0:
            check = self.map[ns-1][we]
            if check == '0':
                north = 1
        
        # check south
        if ns < nslen-1: # at the bottom of the map
            check = self.map[ns+1][we]
            if check == '0':
                south = 1
        
        # check west
        if we > 0:
            check = self.map[ns][we-1]
            if check == '0':
                west = 1
        
        # check east
        if we < welen-1:
            check = self.map[ns][we+1]
            if check == '0':
                east = 1

        return [north, south, west, east]
            
    # Generate an array of initial probabilities
    def initial_probabilities(self):
        
        # count the number of '0'
        k_initial = 0
        for row in self.map:
            for col in row:
                if col == '0':
                    k_initial += 1
        
        self.t0 = deepcopy(self.map)
        i = 0; j = 0
        self.emission_matrix(0)
        for row in self.t0:
            for col in row:
                if col == '0':
                    self.t0[i][j] = ( 1.0/k_initial ) * self.em[i][j]
                else:
                    self.t0[i][j] = 0.0
                j += 1
            j = 0
            i+= 1
        return
    
    # probability of a move in each direction
    def moves(self, ns, we):
        valid_move = self.neighbours(ns, we)

        total = sum(valid_move)
        for n in range(len(valid_move)):
            valid_move[n] = valid_move[n]/total
        return valid_move



    # Generate a transition matrix of size K x K
    def transition_matrix(self):
        i = 0; 
        k = []
        for row in self.map:
            j = 0
            for col in row:
                if self.map[i][j] == '0':

                    k.append([i, j])
                j += 1
            i += 1
        self.traversable = k
        transition_mat = []
        for from_pos in k:
            this_transition = []
            for to_pos in k:
                this_transition.append(is_adjacent(from_pos[0], from_pos[1], to_pos[0], to_pos[1]))
            s = sum(this_transition)
            transition_mat.append(this_transition)
        
        i = 0
        for row in transition_mat:
            s = sum(row)
            if s > 0:
                transition_mat[i] = [j/s for j in transition_mat[i]]
            else:
                transition_mat[i] = 0.0
            i += 1
        self.tm = transition_mat
        return 
    
    def get_transition(self, ns, we):
        if [ns , we] in self.traversable:
            return self.traversable.index([ns,we])
        return 0
    
    # Generate an emission matrix of 
    def emission_matrix(self, t):
        er = self.error_rate
        em_mat = np.ndarray([int(self.dim[0]), int(self.dim[1])], dtype=float) # float
        em_mat = em_mat.tolist()
        # [(1-error)^(4 - d_it)] * error^(d_it)
        i = 0; j = 0
        for row in em_mat:
            for col in row:
                # denotes the number of directions are reporting erroneous values
                d_it = 0
                possible = self.neighbours(i, j)
                
                for p in range(len(possible)):
                    if possible[p] == int(self.obs[t][p]):
                        continue
                    else:
                        d_it += 1
                sensor_correct_prob = (1-self.error_rate) ** (4 - d_it)
                directional_error_rate = self.error_rate ** d_it
                em_mat[i][j] = sensor_correct_prob * directional_error_rate
                j += 1
            j = 0; i += 1
        self.em = em_mat
        return

    def print(self) -> None:
        print('Dimensions: ' + str(self.dim))
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
    # for each position i = 1,2,...,K
        # trellis[i,1] assigned initial_p[i] * Emissions[i][y[0]]

    # 
    view = 0
    if view == 1:
        for row in range(len(m.map)):
            for col in range(len(m.map[0])):
                print(m.neighbours(row, col), end=' ')
            print('')


    # calculate the initial probabilities
    # trellis at 0
    m.initial_probabilities() # also generates em at t=0
    if view == 2:
        for i in range(int(m.dim[0])):
            print(m.t0[i])
    
    m.transition_matrix()
    # trellis at every other observations
    # trellis[s,t] = trellis[k, t-1] * transition[k,i] * emission[i, observation at t]
    
    trellis = [m.t0]
    print(m.t0)
    max_p, pos_max = find_max(m.t0)
    print(max_p)
    print(pos_max)

    time = 1
    for observation in range(len(m.obs) - 1):
        next_trellis = []
        max_p, pos_max = find_max(trellis[time-1])
        transition = m.tm[m.get_transition(pos_max[0], pos_max[1])]
        m.emission_matrix(time) # m.em

        for row in range(int(m.dim[0])):
            row_trellis = []
            for col in range(int(m.dim[1])):
                tindex = m.get_transition(row, col)
                eq = max_p * transition[tindex] * m.em[row][col]
                
                row_trellis.append(eq)
            next_trellis.append(row_trellis)   
        trellis.append(next_trellis)
        time += 1

    ar = 0
    for array in trellis:
        trellis[ar] = np.matrix(array)
        ar += 1
    
    np.savez("output.npz", *trellis)

if __name__ == "__main__":
    main()