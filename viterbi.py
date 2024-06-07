import numpy as np
import sys

def read_input(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    # Map size
    rows, cols = map(int, lines[0].split())

    # Map data
    map_data = []
    for i in range(1, rows + 1):
        map_data.append(lines[i].strip().split())

    # Number of observations
    num_observations = int(lines[rows + 1].strip())

    # Observations
    observations = []
    for i in range(rows + 2, rows + 2 + num_observations):
        observations.append(lines[i].strip())

    # Sensor error rate
    epsilon = float(lines[rows + 2 + num_observations].strip())

    return map_data, observations, epsilon

def get_traversable_positions(map_data):
    traversable_positions = []
    for r, row in enumerate(map_data):
        for c, cell in enumerate(row):
            if cell == '0':
                traversable_positions.append((r, c))
    return traversable_positions

def get_neighbors(map_data, pos):
    r, c = pos
    neighbors = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(map_data) and 0 <= nc < len(map_data[0]) and map_data[nr][nc] == '0':
            neighbors.append((nr, nc))
    return neighbors

def sensor_model(map_data, pos, reading, epsilon):
    r, c = pos
    directions = ['N', 'S', 'W', 'E']
    actual_obstacles = [
        (r - 1 < 0 or map_data[r - 1][c] != '0'),
        (r + 1 >= len(map_data) or map_data[r + 1][c] != '0'),
        (c - 1 < 0 or map_data[r][c - 1] != '0'),
        (c + 1 >= len(map_data[0]) or map_data[r][c + 1] != '0')
    ]
    reading_obstacles = [d in reading for d in directions]
    d_it = sum(1 for a, b in zip(actual_obstacles, reading_obstacles) if a != b)
    return (1 - epsilon) ** (4 - d_it) * epsilon ** d_it

def viterbi(map_data, observations, epsilon):
    traversable_positions = get_traversable_positions(map_data)
    K = len(traversable_positions)
    T = len(observations)
    num_rows = len(map_data)
    num_cols = len(map_data[0])
    
    # Initialize trellis
    trellis = np.zeros((T, num_rows, num_cols))
    
    # Uniform initial probability
    initial_prob = 1 / K
    
    for pos in traversable_positions:
        r, c = pos
        trellis[0, r, c] = initial_prob * sensor_model(map_data, pos, observations[0], epsilon)
    
    # Viterbi forward algorithm
    for t in range(1, T):
        for pos in traversable_positions:
            r, c = pos
            max_prob = 0
            for neighbor in get_neighbors(map_data, pos):
                nr, nc = neighbor
                trans_prob = 1 / len(get_neighbors(map_data, neighbor))
                prob = trellis[t - 1, nr, nc] * trans_prob * sensor_model(map_data, pos, observations[t], epsilon)
                if prob > max_prob:
                    max_prob = prob
            trellis[t, r, c] = max_prob
    
    return trellis

def save_trellis(trellis):
    maps = [trellis[t] for t in range(trellis.shape[0])]
    np.savez("output.npz", *maps)

def main():
    if len(sys.argv) != 2:
        print("Usage: python viterbi.py [input]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    map_data, observations, epsilon = read_input(input_file)
    trellis = viterbi(map_data, observations, epsilon)
    save_trellis(trellis)

if __name__ == "__main__":
    main()
