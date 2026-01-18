#!/usr/bin/env python3
import sys
import os
import pathlib


def count_stats(text):
    lines = text.count('\n')
    words = len(text.split())
    bytes_count = len(text.encode('utf-8'))
    return lines, words, bytes_count


def main():
    total_lines = 0
    total_words = 0
    total_bytes = 0
    file_list = []
    
    if len(sys.argv) > 1:
        for i in range(1, len(sys.argv)):
            filename = sys.argv[i]
            if os.path.exists(filename):
                file_list.append(filename)
            else:
                print(f"wc: {filename}: No such file or directory", file=sys.stderr)
        
        for filename in file_list:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines, words, bytes_count = count_stats(content)

                    print(f"{lines:8}{words:8}{bytes_count:8} {filename}")
                    
                    total_lines += lines
                    total_words += words
                    total_bytes += bytes_count
            except Exception as e:
                print(f"wc: {filename}: {e}", file=sys.stderr)
        
        if len(file_list) > 1:
            print(f"{total_lines:8}{total_words:8}{total_bytes:8} total")
    
    else:
        try:
            content = sys.stdin.read()
            lines, words, bytes_count = count_stats(content)
            print(f"stdin: {lines:8}{words:8}{bytes_count:8}")
        except KeyboardInterrupt:
            sys.exit(0)


if __name__ == "__main__":
    main()