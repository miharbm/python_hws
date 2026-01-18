import sys
import os


def main():
    if len(sys.argv) > 1 and not os.path.exists(sys.argv[1]):
        line_number = 1
        for arg in sys.argv[1:]:
            print(f'{line_number}\t{arg}', end="\n")
            line_number += 1
        else:
            return

    with open(sys.argv[1], 'r', encoding="UTF-8") as f:
        line_number = 1
        for line in f:
            print(f"{line_number}\t{line}", end="")
            line_number += 1

if __name__ == "__main__":
    main()