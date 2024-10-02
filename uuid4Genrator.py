import re
from sys import argv
from uuid import uuid4

def get_words_to_replace(word_file):
    # Read words from the file and return them as a list
    with open(word_file, 'r') as f:
        words = [line.strip() for line in f if line.strip()]
    return words

def main():
    if len(argv) < 2:
        print("Usage: python script.py <words-file>")
        return

    # Read words from the words.txt file
    words_to_replace = get_words_to_replace(argv[1])
    used_var_names = []

    # Sort and reverse to prioritize longer matches
    words_to_replace.sort(key=len, reverse=True)

    # Replace words with UUIDs
    for word in words_to_replace:
        while True:
            new_var_name = uuid4().hex
            # Ensure that the new UUID is not already used
            if new_var_name in used_var_names:
                continue
            else:
                used_var_names.append(new_var_name)
                break
        
        # Print out the word and its corresponding UUID replacement
        print(f"{word} -> {new_var_name}")

if __name__ == "__main__":
    main()
