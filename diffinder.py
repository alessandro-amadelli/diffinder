"""
Diffinder is a python script able to identify all the differences when comparing
two text files.

Author: Ama
"""

import sys
import hashlib
from itertools import zip_longest
from datetime import datetime

def print_logo():
    print("=" * 30)
    print("{:^30}".format("D i f f i n d e r"))
    print("=" * 30)
    print()

    print("Welcome to Diffinder!")
    print("Info:")
    print("Diffinder let's you compare \nfiles and find the lines that \ndiffer between the two.\n")
    print("=" * 30)
    print("\n")

def print_instructions():
    print("INSTRUCTIONS")
    print("1. Execute diffinder")
    print("2. Insert the full path of the first file")
    print("3. Insert the full path of the file against which you want to compare the first one")
    print("4. Diffinder runs and identifies all the lines that differ from one file to the other")
    print("5. Check the resulting file generated for details")
    print()

def calculate_hash(file_name):
    """
    This function takes a file name (path) and reads it in byte mode, returning
    the calculated md5 hash.
    """
    hash_md5 = hashlib.md5()
    with open(file_name, "rb") as f:
        #The file is 'broken down' into consecutive chunks to avoid overload the memory
        CHUNK_LENGTH = 4096
        for chunk in iter(lambda: f.read(CHUNK_LENGTH), b""):
            hash_md5.update(chunk)

    return hash_md5.hexdigest()

def compare_files(file1, file2):
    """
    This function takes 2 file name (path) and reads the files line by line, comparing
    the resulting strings.
    The lines that differ are then written to a file.
    The number of differences found is then returned.
    """
    #Timestamp of comparison
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tm2 = timestamp.replace(":",".")

    #file that will contain all the lines that differ
    file_out = f".\{tm2}_variations.txt"

    line_count, diff_count = 0,0

    f_out = open(file_out, "w")
    f_out.write(f"Comparison started: {timestamp}\n")

    with open(file1, "r") as f1, open(file2, "r") as f2:
        for line1, line2 in zip_longest(f1,f2):
            line_count += 1
            line1 = (line1 if line1 != None else "")
            line2 = (line2 if line2 != None else "")

            if (line1:=line1.strip()) != (line2:=line2.strip()):
                diff_count += 1
                f_out.write("=" * 30 + "\n")
                f_out.write(f"LINE #{line_count}\n")
                f_out.write("=" * 30 + "\n")
                f_out.write(f"{file1}: \n{line1}\n")
                f_out.write(f"{file2}: \n{line2}\n\n")
    f_out.close()

    return diff_count


def main():
    #Diffinder welcome
    print_logo()

    #Users choice
    print("Select an option:")
    print("{:5}".format("i"), "Instructions", sep="")
    print("{:5}".format("c"), "Start compare", sep="")
    print("{:5}".format("q"), "Quit", sep="")
    option  = input("Option: ")

    if option == "i":
        print_instructions()
    elif option == "c":
        print("Starting compare")
    elif option == "q":
        print("Quitting...")
        sys.exit()
    else:
        print("Wrong choice...I quit!")
        sys.exit()

    #Input files to compare
    file1 = input("Enter full path of the first file: ")
    file2 = input("Enter full path of the second file: ")

    #Calculating file hashes for a first quick comparison between the two
    file1_hash = calculate_hash(file1)
    file2_hash = calculate_hash(file2)
    print(file1_hash, file2_hash, sep="\n")

    #Two identical hashes means the two files are identical
    if file1_hash == file2_hash:
        print("== The two files are identical. ==")
        return True

    print("!! Differences found. !!")
    diff_count = compare_files(file1, file2)
    print(f"TOTAL DIFFERENCES FOUND: {diff_count}")
    print("Details can be found in file: \"variations.txt\".")

if __name__ == "__main__":
    main()
