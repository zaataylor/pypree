From the `man` page:
> Tree is a recursive directory listing program that produces a depth indented listing of files, which is colorized ala dircolors if the LS_COLORS environment variable is set and output is to tty. With no arguments, tree lists the files in the current directory. When directory arguments are given, tree lists all the files and/or directories found in the given directories each in turn.  Upon completion of listing all files/directories found, tree returns the total number of files and/or directories listed.

Main Things I Need To Do:
- `TreeItem` class
    - Plan: make a `TreeItem` class that'll recursively hold the values of the files and directories below it in the form of `TreeItem`s. Then, print out this tree recursively with some nice-looking formatting, maybe using `pprint`?
    - `TreeItem` has:
        - Name
        - IsDir
        - Children (which are `TreeItem`s)
- Function to print out the contents of a `TreeItem`
- Function to create the Tree
    - Strategy here is to recurse down until we get a regular file, then we construct a basic `TreeItem` that is not a directory (or an empty directory) and return it. This will be appended to the children member of the `TreeItem` corresponding to the parent of that `TreeItem`.
- Function to get total count of directories and files