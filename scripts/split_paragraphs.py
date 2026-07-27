#!/usr/bin/env python3
import os
import sys

def split_file(input_filename, prefix, postfix='en', num_parts=10):
    with open(input_filename, 'r') as f:
        content = f.read()

    lines = content.splitlines(keepends=True)
    target = len(lines) // num_parts
    parts = []
    start = 0
    for i in range(num_parts - 1):
        end = start + target
        while end < len(lines) and lines[end].strip() != '':
            end += 1
        if end < len(lines):
            parts.append(''.join(lines[start:end+1]))
        else:
            parts.append(''.join(lines[start:]))
            start = len(lines)
            break
        start = end + 1

    if start < len(lines):
        parts.append(''.join(lines[start:]))

    for i, part in enumerate(parts[:num_parts]):
        filename = f'{prefix}-{i:02d}-{postfix}.md'
        with open(filename, 'w') as f:
            f.write(part)

    print(f'Created {len(parts)} files.')

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python split_paragraphs.py <input_file> <prefix> [postfix] [num_parts]")
    else:
        p = sys.argv[3] if len(sys.argv) > 3 else 'en'
        n = int(sys.argv[4]) if len(sys.argv) > 4 else 10
        split_file(sys.argv[1], sys.argv[2], p, n)
