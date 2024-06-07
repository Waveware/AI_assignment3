import numpy as np

def load_trellis(file_path):
    try:
        data = np.load(file_path)
        trellis = [data[key] for key in data.files]
        return trellis
    except Exception as e:
        print("Error loading trellis matrix:", e)
        return None

def compare_trellis_matrices(matrix_a, matrix_b):
    if len(matrix_a) != len(matrix_b):
        print("Number of time steps in the two trellis matrices is different.")
        return

    for t in range(len(matrix_a)):
        if not np.array_equal(matrix_a[t], matrix_b[t]):
            print(f"Time Step {t}:")
            print("Matrix A:")
            print(matrix_a[t])
            print("Matrix B:")
            print(matrix_b[t])
            print()

def main():
    file_path_a = input("Enter the file path for trellis matrix A: ")
    file_path_b = input("Enter the file path for trellis matrix B: ")

    trellis_a = load_trellis(file_path_a)
    trellis_b = load_trellis(file_path_b)

    if trellis_a is not None and trellis_b is not None:
        compare_trellis_matrices(trellis_a, trellis_b)
        print("Comparison complete.")

if __name__ == "__main__":
    main()
