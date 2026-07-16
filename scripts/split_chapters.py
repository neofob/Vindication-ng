import re
import os

def split_chapters(input_file, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Find the first occurrence of "CHAPTER 1." that is actually the start of the book, not TOC
    # Looking at grep output, TOC is ~400 and Book starts at ~1017
    start_line = -1
    for i in range(len(lines)):
        if lines[i].startswith('CHAPTER 1.'):
            # Heuristic: The actual Chapter 1 usually has a title or is followed by more text, 
            # and the TOC entries are closely packed. 
            # Let's specifically skip the first few occurrences if they are in the TOC block.
            if i > 500: # Based on our grep, actual book starts after line 1000
                start_line = i
                break

    if start_line == -1:
        print("Could not find the start of Chapter 1.")
        return

    chapters = []
    current_chapter_content = []
    chapter_num = 0

    for i in range(start_line, len(lines)):
        line = lines[i]
        match = re.match(r'^CHAPTER (\d+)\.', line)
        if match:
            if current_chapter_content:
                chapters.append((''.join(current_chapter_content), chapter_num))
            
            chapter_num = int(match.group(1))
            current_chapter_content = [line]
        else:
            current_chapter_content.append(line)

    # Append the last chapter
    if current_chapter_content:
        chapters.append((''.join(current_chapter_content), chapter_num))

    for content, num in chapters:
        filename = f"ch-{num:02d}-en.md"
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            # Simple conversion to Markdown: keep content as is, 
            # but the CHAPTER line is already a good header candidate.
            f.write(content)
        print(f"Saved {filename}")

if __name__ == "__main__":
    split_chapters('/home/tuan/src/Vindication/pg3420.txt', '/home/tuan/src/Vindication/chapters')
