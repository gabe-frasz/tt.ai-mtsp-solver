from src.mtsp import mTSP


def main():
    cities = [
        (0, 0),
        (1, 0),
        (2, 0),
        (3, 0),
        (4, 0),
        (5, 0),
        (6, 0),
    ]

    depot = (30, 30)

    mtsp = mTSP(cities, depot)

    print(mtsp.valid_genes)

    for i in range(8):
        for j in range(8):
            print(f"{mtsp.distance_matrix[i][j]:.2f}", end=" ")
        print()


if __name__ == "__main__":
    main()
