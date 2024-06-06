import sys
import numpy as np
import viterbi


def compare_npz(file_path1, file_path2):
    file1 = np.load(file_path1,allow_pickle=True)
    file2 = np.load(file_path2,allow_pickle=True)
    # Check if the files have the same keys
    keys1 = set(file1.files)
    keys2 = set(file2.files)

    if keys1 != keys2:
        print("Files have different keys")
        return

    for key in keys1:
        arr1 = file1[key]
        arr2 = file2[key]

        # Compare shapes
        if arr1.shape != arr2.shape:
            print(f"Different shapes for key {key}: {arr1.shape} vs {arr2.shape}")
            continue

        # Compare values
        if np.array_equal(arr1, arr2):
            print(f"Arrays are equal for key {key}")
        else:
            for i in range(arr1.shape[0]):
                for j in range(arr1.shape[1]):
                    if arr1[i][j] != arr2[i][j]:
                        print(f"Arrays are different for key {key}, index: i:{i}, j:{j}, computed: {arr1[i][j]},expected: {arr2[i][j]}")
    file1.close()
    file2.close()




def main():

    input_file_path = sys.argv[1]
    correct_file_path = sys.argv[2]

    compare_npz('output.npz', correct_file_path)

if __name__ == "__main__":
    main()