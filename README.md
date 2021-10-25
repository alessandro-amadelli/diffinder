# Diffinder
## Diffinder is a python script that helps you analyze differences between 2 files.

### Instructions
1. Execute diffinder
2. Insert the full path of the first file
3. Insert the full path of the file against which you want to compare the first one
4. Diffinder runs and identifies all the lines that differ from one file to the other
5. Check the resulting file generated for details

### Notes
The first operation diffinder performs is to generate and check the MD5 hash digest of
the two files.
If the digests correspond, than the two files are identical.
Otherwise, diffinder reads the files line by line, writing in the resulting file information
about the different lines so you can easily refer them to the original files.

Files containing details about the variations are saved with the following name structure:
**YYYY-MM-DD HH.mm.ss_variations.txt** 
So you can modify a file and regenerate the result without loosing the change history.
