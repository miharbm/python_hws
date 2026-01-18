import sys
import os
import pathlib


def main():
    file_list = []
    if len(sys.argv) > 1:
        for i in range(1, len(sys.argv)):
            if os.path.exists(sys.argv[i]):
                file_list.append(sys.argv[i])
        for file in file_list:
            if len(file_list) > 1:
                print(f"File: {pathlib.Path(file).name}")
            with open(file, 'r', encoding="UTF-8") as f:
                lines = f.readlines()
                last_10 = lines[-10:]
                for line in last_10:
                    print(line.rstrip())
            if len(file_list) > 1 and file != file_list[-1]:
                print()

    if not file_list:
        lines = sys.stdin.readlines()
        last_17 = lines[-17:]
        for line in last_17:
            print(line.rstrip())

if __name__ == "__main__":
    main()