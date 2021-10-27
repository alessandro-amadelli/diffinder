"""
Diffinder is a python script able to identify all the differences when comparing
two text files.

Author: Ama
"""

import sys
import os
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

def initial_user_choice():
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
    try:
        with open(file_name, "rb") as f:
            #The file is 'broken down' into consecutive chunks to avoid overload the memory
            CHUNK_LENGTH = 4096
            for chunk in iter(lambda: f.read(CHUNK_LENGTH), b""):
                hash_md5.update(chunk)
    except FileNotFoundError:
        print(f"File '{file_name}' not found. Please check the file name...")
        sys.exit()
    except:
        print(f"Error opening file '{file_name}'")
        sys.exit()

    return hash_md5.hexdigest()

def get_file_size(file_name):
    """
    The function uses the os package to get the size of a specified file.
    Then the file size is converted in the most suitable unit.
    The file size is returned alogn with the size unit.
    """
    size = os.path.getsize(file_name)

    if size in range(0, 1024):
        file_size = size
        size_unit = "B"
    elif size in range(1024, 1024 * 1000):
        file_size = size / 1024
        size_unit = "KB"
    elif size in range (1024 * 1000, 1024 * 1000 * 1000):
        file_size = size / 1024 / 1024
        size_unit = "MB"
    else:
        file_size = size / 1024 /1024 /1024
        size_unit = "GB"

    file_size = "{:.2f}".format(file_size)

    return file_size, size_unit

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
    f_out.write("VARIATIONS FILE\nWords in unchanged between the two lines are represented by an underscore ( '_' )\n" \
    f"Comparison started: {timestamp}\n")

    with open(file1, "r") as f1, open(file2, "r") as f2:
        for line1, line2 in zip_longest(f1,f2):
            line_count += 1
            line1 = (line1 if line1 != None else "")
            line2 = (line2 if line2 != None else "")

            if (line1:=line1.strip()) != (line2:=line2.strip()):
                diff_count += 1

                #Finding different words in line of second file
                str2 = ""
                split1, split2 = line1.split(), line2.split()
                c_num = min(len(split1),len(split2))
                for i in range(c_num):
                    if split1[i] == split2[i]:
                        str2 += "_" * len(split1[i])
                    else:
                        str2 += split2[i]
                    str2 += " "

                if len(line2) > len(line1):
                    str2 += " ".join(split2[i+1:])

                f_out.write("=" * 30 + "\n" + f"LINE #{line_count}\n" + "=" * 30 + "\n" \
                f"{file1}: \n{line1}\n" \
                f"{file2}: \n{str2}\n\n")
    f_out.close()

    return [diff_count, file_out]

def main():
    #Diffinder welcome
    print_logo()

    #User options
    initial_user_choice()

    #Input files to compare + hash calculation for a first quick comparison
    file1 = input("Enter full path of the first file: ")
    file1_hash = calculate_hash(file1)
    file2 = input("Enter full path of the second file: ")
    file2_hash = calculate_hash(file2)
    # print(file1_hash, file2_hash, sep="\n")

    #get file sizes to informate the user
    file1_size, size1_unit = get_file_size(file1)
    file2_size, size2_unit = get_file_size(file2)
    print("File sizes:")
    print("{:50}".format(f"{file1}:") + "{:>20}".format(f"{file1_size} {size1_unit}"),
          "{:50}".format(f"{file2}:") + "{:>20}".format(f"{file2_size} {size2_unit}"), sep="\n")
    print()

    #Two identical hashes means the two files are identical
    if file1_hash == file2_hash:
        print("== The two files are identical. ==")
        return True

    print("!! Differences found. !!")
    diff_count = compare_files(file1, file2)
    print(f"TOTAL DIFFERENCES FOUND: {diff_count[0]}")
    print(f"Details can be found in file: \"{diff_count[1]}\".")

if __name__ == "__main__":
    main()
