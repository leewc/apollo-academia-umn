# A3-Utils
# F2015 CSCI 4061 Assignment/Lab 3 : ls -l, grep, find
# Name : Wen Chuan Lee (leex7095)

#Introduction 

3 OS utilities were implemented in C:
    ls -l 
    grep
    find

The programs written emulate the system utilities found on Unix systems.

# Building

Run `make` or manually build each utility like so:
    gcc ls.c -o ls
    gcc grep.c -o grep
    gcc find.c -o find

# Usage

For ls -l:
    `./ls` or `./ls <filename or dir>`
    
For grep:
    ./grep <string> <filename>

.. where string is the string to search for in the file.

For find:
    ./find <filename> <starting directory>
    
# Additional Notes and Design

Each program implements very basic features of each utility. As such it was all placed in one file. 

## `ls` 
1. The program emulates the real `ls -l` implementation, in which it prints the read, write, execute permissions, the group and owner of the file, the filesize, and time modified alonf with the filename. 
2. The program iteratively walks through a directory with the use of `dirent` and gets file stats with `stat`.
3. Bitwise ANDs were used in one-line conditionals to avoid a clutter of if-else statements.
4. A `displayInfo` function was written to display information about a file, this is immediately called if a filename is given as an input parameter. 
5. A `displayFiles` function was written to call `displayInfo` on each file in a directory, these helper functions ensured not everything was stuck into the `main` function.

## `grep`
1. The program is able to search for a string or substring within a regular file, printing the line no and the line where the word was found.
2. `grep` works by first checking if the given filename for a file actually exists, and if it is an actual file using `stat`,
3. It then opens the file as a stream with the `fopen` method.
4. After which each line is read using `getline` (as `fgets` is considered old (have to allocate buffer manually, and `gets` is deprecated.)
5. Should the string be found (using `strstr` function), the entire string is printed along with the line number.
6. Nothing is displayed if the file was not found.
7. As this `grep` implementation is not hard, there is only one function that actually opens and reads the file after the it is properly checked for (in the main method).

## `find`
1. THe program recursively walks down the starting directory, keeping track of paths.
2. An error is printed if the file/dir cannot be opened or stat with `dirent` or `stat` (e.g when there the user has insufficient permissions or invalid file path)
3. This version of find works on symlinks and will follow the symlinks, this was done with `stat` (gets stats of the file) instead of `lstat` (gets stats of the link itself)
4. If a file is found the file path and name will be displayed.
5. Helper functions were used to traverse down directories, recursion was used as we are able to traverse down many dierectories that way with the stack keeping track of the file names.
5. Nothing is displayed if a file was not file. Nothing is displayed if the file was not found.

All utilities handle freeing of memory and closing file descriptors as well (I think).