import numpy as np
import sys

def print_npz_contents(file_path):
    npz_file = np.load(file_path)
    for key in npz_file.keys():
        print(f"Key: {key}")
        print(npz_file[key])

def main(file_path):
    print_npz_contents(file_path)

if __name__ == "__main__":
    npz_file_path = sys.argv[1]
    main(npz_file_path)
